
$(document).ready(function(){
$("#menu-toggle-2").click(function(e){
        e.preventDefault();
        $("#canvas").toggleClass("toggled");
    });
    //getLagislatorDetails();    
});


function slideNext() {
    $("#legislator_carousal").carousel(1);
}


function slidePrev() {
    $("#legislator_carousal").carousel(0);
}


function getDisplayValue(str1,str2){
    returnStr="";
    if (str2==null){
        returnStr="N.A";
    }else{
        returnStr=str1+str2;
    }
    return returnStr;
    
}




var app = angular.module('myApp', ['angularUtils.directives.dirPagination']);
app.controller('Legislator', function($scope, $http) {
    $http.get("https://congress.api.sunlightfoundation.com/legislators?apikey=9333ff0e107c475da428e3df914716ef&per_page=all")
    .then(function(response) {
    $scope.selectedData = response.data;
    $scope.SelectedName = 'Legislator';
    $scope.parsedJson=angular.fromJson($scope.selectedData.results);
    $scope.valueHouse='house'
    $scope.valueSenate='senate'
    });
    
    $scope.getLegislatorDetails=function(bioguide){
        slideNext();
    $http.get("https://congress.api.sunlightfoundation.com/legislators?apikey=9333ff0e107c475da428e3df914716ef&bioguide_id="+bioguide)
    .then(function(response) {
    $scope.selectedData = response.data;
    
    $scope.parsedJsonBioguide=angular.fromJson($scope.selectedData.results);
    $scope.parsedJsonBioguide=$scope.parsedJsonBioguide[0];
    
    $scope.bioguideImg="https://theunitedstates.io/images/congress/original/"+bioguide+".jpg";
    $scope.LegisDispName=$scope.parsedJsonBioguide.title +"."+ $scope.parsedJsonBioguide.last_name +","+$scope.parsedJsonBioguide.first_name;
    //chamberName=$scope.parsedJsonBioguide.chamber.charAt(0).toUpperCase()
    $scope.LegisDispChamber=getDisplayValue("Chamber: ",$scope.parsedJsonBioguide.chamber.charAt(0).toUpperCase()+$scope.parsedJsonBioguide.chamber.substr(1));
    $scope.LegisDispEmail=getDisplayValue("",$scope.parsedJsonBioguide.oc_email);
    $scope.LegisDispPhone=getDisplayValue("Contact:",$scope.parsedJsonBioguide.phone);
    party=$scope.parsedJsonBioguide.party;
    switch(party){
        case 'R':
            $scope.LegisDispPartyImg="http://cs-server.usc.edu:45678/hw/hw8/images/r.png";
            $scope.LegisDispPartyNm="Republican";
        break;
        case 'D':
            $scope.LegisDispPartyImg="http://cs-server.usc.edu:45678/hw/hw8/images/d.png";
            $scope.LegisDispPartyNm="Democrat";
        break;
        
        default:
            $scope.LegisDispPartyImg="http://independentamericanparty.org/wp-content/themes/v/images/logo-american-heritage-academy.png";
            $scope.LegisDispPartyNm="Independent";
        break;
    }
    $scope.LegisDispTermStart=getDisplayValue("",$scope.parsedJsonBioguide.term_start);
    $scope.LegisDispTermEnd=getDisplayValue("",$scope.parsedJsonBioguide.term_end);
    $scope.LegisDispTerm=
    $scope.LegisDispTermOfc=getDisplayValue("",$scope.parsedJsonBioguide.office);
    $scope.LegisDispState=getDisplayValue("",$scope.parsedJsonBioguide.state_name);
    $scope.LegisDispFax=getDisplayValue("",$scope.parsedJsonBioguide.fax);
    $scope.LegisDispBirth=getDisplayValue("",$scope.parsedJsonBioguide.birthday);
    $scope.today = new Date();
    $scope.LegisDispTerm=($scope.today -$scope.LegisDispTermStart) / ($scope.LegisDispTermEnd - $scope.LegisDispTermStart) * 100;
    $scope.LegisFBId=getDisplayValue("http://www.facebook.com/",$scope.parsedJsonBioguide.facebook_id)
    if ($scope.parsedJsonBioguide.facebook_id==null){
        $scope.facebookImg=""
    } else{
        $scope.facebookImg="http://cs-server.usc.edu:45678/hw/hw8/images/f.png"
    }
    $scope.LegisTwTId=getDisplayValue("http://www.twitter.com/",$scope.parsedJsonBioguide.twitter_id)
    if ($scope.parsedJsonBioguide.twitter_id==null){
        $scope.twitterImg=""
    } else{
        $scope.twitterImg="http://cs-server.usc.edu:45678/hw/hw8/images/t.png"
    }
    $scope.LegisWebSite=getDisplayValue("",$scope.parsedJsonBioguide.website)
    if ($scope.parsedJsonBioguide.website==null){
        $scope.webImg=""
    } else{
        $scope.webImg="http://cs-server.usc.edu:45678/hw/hw8/images/w.png"
    }
    
    $http.get("https://congress.api.sunlightfoundation.com/committees?apikey=9333ff0e107c475da428e3df914716ef&member_ids="+bioguide+"&per_page=5")
    .then(function(response) {
    $scope.selectedDataCommittee = response.data;
    $scope.parsedJsonBioguideCommitte=angular.fromJson($scope.selectedDataCommittee.results);
    });
    
    
    $http.get("https://congress.api.sunlightfoundation.com/bills?apikey=9333ff0e107c475da428e3df914716ef&sponsor_id="+bioguide+"&per_page=5")
    .then(function(response) {
    $scope.selectedDataBill = response.data;
    $scope.parsedJsonBioguideBill=angular.fromJson($scope.selectedDataBill.results);
    });
    
    
    
    });
        
        
    }
    
    
    
    $scope.slidePrev=function(){
        slidePrev();
    }
});




app.controller('Bills', function($scope, $http) {
    
    $http.get("https://congress.api.sunlightfoundation.com/legislators?apikey=9333ff0e107c475da428e3df914716ef&per_page=all")
    .then(function(response) {
    $scope.myWelcome = response.data;
    $scope.SelectedName = 'Bills';
    
    });


});
