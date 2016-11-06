$(document).ready(function(){
$("#menu-toggle-2").click(function(e){
        
        $("#canvas").toggleClass("toggled");
    });
    localStorage.clear();
    
});


function slideNext() {
    $("#legislator_carousal").carousel(1);
}

function slideNextBill() {
    $("#bill_carousal").carousel(1);
}


function slidePrev() {
    $("#legislator_carousal").carousel(0);
}

function slidePrevBill() {
    $("#bill_carousal").carousel(0);
}


function addToLocalStorage(key,value){
    localStorage.setItem(key,value);
    console.log(localStorage);
}

function callJSFav(){

    var scope = angular.element(document.getElementById("FavoriteTab")).scope();
    scope.getFavBills();
    scope.getFavLegs();
    scope.getFavComs();
//    $("#FavoriteTab").addClass('active');
//    $("#output").removeClass('active');
//    alert("Fav JS")
}

function callJSFavClick(){

    var scope = angular.element(document.getElementById("FavoriteTab")).scope();
    scope.getFavBills();
    scope.getFavLegs();
    scope.getFavComs();
    $("#FavoriteTab").addClass('active');
    $("#output").removeClass('active');
    $("#outputBill").removeClass('active');
    //alert("Fav JS")
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

function deleteStar(inArr,Id){
    inArr[Id] ? delete inArr[Id] : inArr[Id]=1
}


function getFavLegDetailsJS(bioguide_id){
    var scope = angular.element(document.getElementById("output")).scope();
    scope.getLegislatorDetails(bioguide_id);
//    $("#legislator_carousal").carousel(1);
    $("#output").addClass('active');
    $("#FavoriteTab").removeClass('active');
    
    
}


function getFavBillDetailsJS(bill_id){
    var scope = angular.element(document.getElementById("outputBill")).scope();
    scope.getBillsDetails(bill_id);
    //$("#bill_carousal").carousel(1);
    $("#outputBill").addClass('active');
    $("#FavoriteTab").removeClass('active');

    
    
    
    
    
    
    
    
    
}



var app = angular.module('myApp', ['angularUtils.directives.dirPagination']);
app.service('sharedProperties', function () {
        var comIdArr = {};
        var legIdArr = {};
        var billIdArr = {};
        return {
            getStarComProperty: function () {
                return comIdArr;
            },
            getStarLegProperty: function () {
                return legIdArr;
            },
            getStarBillProperty: function () {
                return billIdArr;
            }
        };
    });

app.controller('Legislator', function($scope, $http, sharedProperties) {
    $http.get("https://congress.api.sunlightfoundation.com/legislators?apikey=9333ff0e107c475da428e3df914716ef&per_page=all")
    .then(function(response) {
    $scope.selectedData = response.data;
    $scope.SelectedName = 'Legislator';
    $scope.parsedJson=angular.fromJson($scope.selectedData.results);
    $scope.valueHouse='house'
    $scope.valueSenate='senate'
    });
    
    $scope.getLegislatorDetails=function(bioguide){
        $scope.bioguide=bioguide;
        
        slideNext();
    $http.get("https://congress.api.sunlightfoundation.com/legislators?apikey=9333ff0e107c475da428e3df914716ef&bioguide_id="+bioguide)
    .then(function(response) {
        $scope.selectedData = response.data;
        
        $scope.parsedJsonBioguide=angular.fromJson($scope.selectedData.results);
        $scope.parsedJsonBioguide=$scope.parsedJsonBioguide[0];
        
        $scope.bioguideImg="https://theunitedstates.io/images/congress/original/"+bioguide+".jpg";
        $scope.LegisDispName=$scope.parsedJsonBioguide.title +"."+ $scope.parsedJsonBioguide.last_name +","+$scope.parsedJsonBioguide.first_name;
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
        $scope.LegisDispOfc=getDisplayValue("",$scope.parsedJsonBioguide.office);
        $scope.LegisDispState=getDisplayValue("",$scope.parsedJsonBioguide.state_name);
        $scope.LegisDispFax=getDisplayValue("",$scope.parsedJsonBioguide.fax);
        $scope.LegisDispBirth=getDisplayValue("",$scope.parsedJsonBioguide.birthday);
        $scope.today = new Date();
        $scope.LegisDispTerm=50;
        //($scope.LegisDispTermEnd.getFullYear()-$scope.LegisDispTermStart.getFullYear()) + ($scope.LegisDispTermEnd.getMonth()-$scope.LegisDispTermStart.getMonth())/12 + ($scope.LegisDispTermEnd.getDate()-$scope.LegisDispTermStart.getDate())/365
        //($scope.today -$scope.LegisDispTermStart) / ($scope.LegisDispTermEnd - $scope.LegisDispTermStart) * 100;
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
            
         
    
    //
//  
        $scope.addToLocalStorage=function(){
            $scope.legIdArr=sharedProperties.getStarLegProperty();
            $scope.bioguide=$scope.bioguide;
            deleteStar($scope.legIdArr,$scope.bioguide)
            legsKey="Legs";

            var legsArr = localStorage[legsKey] ? JSON.parse(localStorage[legsKey]) : [];
            var exists=false;
            for (j=0;j<legsArr.length;j++)
                {
                    if (legsArr[j].bioguide_id == $scope.bioguide){
                        legsArr.splice(j,1);
                        exists=true;
                    }
                }
            if (exists==false)
                legsArr.push(this.parsedJsonBioguide);
                
            
            localStorage[legsKey]=JSON.stringify(legsArr);
            callJSFav();
        }
   
    }
    
    
    
    $scope.slidePrev=function(){
        slidePrev();
    }
});








app.controller('Bills', function($scope, $http, sharedProperties) {
    
    $http.get("https://congress.api.sunlightfoundation.com/bills?apikey=9333ff0e107c475da428e3df914716ef&per_page=50")
    .then(function(response) {
    $scope.selectedDataBills = response.data;
    $scope.parsedJsonBills=angular.fromJson($scope.selectedDataBills.results); 
    $scope.activeBill=true;
    $scope.newBill=false;
    });

    
    $scope.getBillsDetails=function(bill_id){
        $scope.bill_id=bill_id;
        slideNextBill();
        $http.get("https://congress.api.sunlightfoundation.com/bills?apikey=9333ff0e107c475da428e3df914716ef&bill_id="+bill_id)
    .then(function(response) {
        $scope.selectedDataBillsId = response.data;
        $scope.parsedJsonBillsId=angular.fromJson($scope.selectedDataBillsId.results); 
        $scope.parsedJsonBillsId=$scope.parsedJsonBillsId[0];
        $scope.BillDispID=getDisplayValue("",$scope.parsedJsonBillsId.bill_id);
        $scope.BillDispTitle=getDisplayValue("",$scope.parsedJsonBillsId.official_title);
        $scope.BillDispType=getDisplayValue("",$scope.parsedJsonBillsId.bill_type);
        $scope.BillDispSponsor=getDisplayValue("",$scope.parsedJsonBillsId.sponsor.title+"."+  $scope.parsedJsonBillsId.sponsor.last_name+", "+ $scope.parsedJsonBillsId.sponsor.first_name);
        $scope.BillDispChamber=getDisplayValue("",$scope.parsedJsonBillsId.chamber);
        if ($scope.parsedJsonBillsId.history.active)
            $scope.BillDispStatus="Active";
        else
            $scope.BillDispStatus="New";
        $scope.BillDispIntro=getDisplayValue("",$scope.parsedJsonBillsId.introduced_on);
        $scope.BillDispCURI=getDisplayValue("",$scope.parsedJsonBillsId.urls.congress);
        $scope.BillDispVer=getDisplayValue("",$scope.parsedJsonBillsId.last_version.version_name);
        $scope.BillDispBURI=getDisplayValue("",$scope.parsedJsonBillsId.last_version.urls.pdf);
    });
        
        $scope.addToLocalStorage=function(){
            $scope.billIdArr=sharedProperties.getStarBillProperty();
            $scope.bill_id=$scope.bill_id;
            deleteStar($scope.billIdArr,$scope.bill_id)

            billKey="Bills";
            var billArr = localStorage[billKey] ? JSON.parse(localStorage[billKey]) : [];
            var exists=false;
            for (j=0;j<billArr.length;j++)
                {
                    if (billArr[j].bill_id == $scope.bill_id){
                        billArr.splice(j,1);
                        exists=true;
                    }
                }
            if (exists==false)
                billArr.push(this.parsedJsonBillsId);

            localStorage[billKey]=JSON.stringify(billArr);
            callJSFav();
            
        }
    
    }
    
    $scope.slidePrevBill=function(){
        slidePrevBill();
    }
    
    
    
    
});







app.controller('Committe', function($scope, $http, sharedProperties) {
    
    
    
    $http.get("https://congress.api.sunlightfoundation.com/committees?apikey=9333ff0e107c475da428e3df914716ef&per_page=all")
    .then(function(response) {
    $scope.selectedDataCommittee = response.data;
    $scope.parsedJsonCommitte=angular.fromJson($scope.selectedDataCommittee.results); 
    console.log($scope.parsedJsonCommitte);
    });
    
    $scope.val=0;
    $scope.comIdArr=sharedProperties.getStarComProperty();
    
    $scope.addToLocalStorage=function(comId){
        deleteStar($scope.comIdArr,comId)
//            $scope.idArr[comId] ? delete $scope.idArr[comId] : $scope.idArr[comId]=1
            
            
        
        
        commKey="Comm";
        var commArr = localStorage[commKey] ? JSON.parse(localStorage[commKey]) : [];
        var n=angular.fromJson(this.parsedJsonCommitte).length;
        for (var i=0;i<n;i++){
            var exists=false;
            if (angular.fromJson(this.parsedJsonCommitte)[i]["committee_id"]==comId){
//                var json = JSON.parse(localStorage[commKey]);

                    for (j=0;j<commArr.length;j++)
                    {
                        if (commArr[j].committee_id == comId){
                            commArr.splice(j,1);
                            exists=true;
                        }
                    }
                    if (exists==false)
                    commArr.push(angular.fromJson(this.parsedJsonCommitte)[i]);
            }
                
                
            }
        
        localStorage[commKey]=JSON.stringify(commArr);
        callJSFav();
    }
    

    
});













app.controller('Favorite', function($scope, $http, sharedProperties) {
        $scope.isactive=($scope.isactive)%2;
        $scope.selectedFavBS=localStorage["Bills"];
        $scope.parsedJsonFavBS1=angular.fromJson($scope.selectedFavBS); 
        $scope.parsedJsonFavBS2=angular.fromJson($scope.parsedJsonFavBS1); 
        $scope.parsedJsonFavBSA=[];
        $scope.parsedJsonFavBS={};

        
        $scope.getFavBills=function()
        {
            if (localStorage["Bills"])
            {

                $scope.selectedFavBS=localStorage["Bills"];
                $scope.parsedJsonFavBS1=angular.fromJson($scope.selectedFavBS); 
                $scope.parsedJsonFavBS2=angular.fromJson($scope.parsedJsonFavBS1); 
                $scope.parsedJsonFavBSA=[];
                $scope.parsedJsonFavBS={};
                
                for (var i=0;i<$scope.parsedJsonFavBS2.length;i++)
                {
                    var chk=false;
                        for (var j=0; j <$scope.parsedJsonFavBSA.length;j++)
                        {
                            if (angular.fromJson($scope.parsedJsonFavBS2[i]).bill_id == angular.fromJson($scope.parsedJsonFavBSA[j]).bill_id)
                            {
                                chk=true;
                                break;
                            }
                        }
                                
                        if (chk==false){
                            $scope.parsedJsonFavBSA.push(angular.fromJson($scope.parsedJsonFavBS2[i]));
                        }
                            
                }
                    
                    $scope.parsedJsonFavBS=angular.fromJson($scope.parsedJsonFavBSA)
                    console.log($scope.parsedJsonFavBS);
            }  
            
        }
        $scope.getFavBillDetails=function(bill_id){
        getFavBillDetailsJS(bill_id)
        
        }







    $scope.selectedFavLS=localStorage["Legs"];
    
    $scope.parsedJsonFavLS2=angular.fromJson($scope.selectedFavLS); 
    $scope.parsedJsonFavLSA=[];
    $scope.parsedJsonFavLS={};

        
    $scope.getFavLegs=function()
    {
        
        if (localStorage["Legs"])
        {
            $scope.selectedFavLS=localStorage["Legs"];
            
            $scope.parsedJsonFavLS2=angular.fromJson($scope.selectedFavLS); 
            $scope.parsedJsonFavLSA=[];
            $scope.parsedJsonFavLS={};
            
            
            
            for (var i=0;i<$scope.parsedJsonFavLS2.length;i++)
            {
                var chk=false;
                    for (var j=0; j <$scope.parsedJsonFavLSA.length;j++)
                    {
                        if (angular.fromJson($scope.parsedJsonFavLS2[i]).bioguide_id == angular.fromJson($scope.parsedJsonFavLSA[j]).bioguide_id)
                        {
                            chk=true;
                            break;
                        }
                    }
                            
                    if (chk==false)
                    {
                        $scope.parsedJsonFavLSA.push(angular.fromJson($scope.parsedJsonFavLS2[i]));
                    }
                        
            }
                
                $scope.parsedJsonFavLS=angular.fromJson($scope.parsedJsonFavLSA)
                console.log($scope.parsedJsonFavLS);
        }    
    }
    $scope.getFavLegDetails=function(bioguide_id){
        getFavLegDetailsJS(bioguide_id)
        
    }

    
    
    
    $scope.getFavComs=function(){
        
        if (localStorage["Comm"])
        {
            $scope.selectedFavCS=localStorage["Comm"];
            
            $scope.parsedJsonFavCS2=angular.fromJson($scope.selectedFavCS); 
            $scope.parsedJsonFavCSA=[];
            $scope.parsedJsonFavCS={};
            
            
            for (var i=0;i<$scope.parsedJsonFavCS2.length;i++)
            {
                var chk=false;
                    for (var j=0; j <$scope.parsedJsonFavCSA.length;j++)
                    {
                        if (angular.fromJson($scope.parsedJsonFavCS2[i]).committee_id == angular.fromJson($scope.parsedJsonFavCSA[j]).committee_id)
                        {
                            chk=true;
                            break;
                        }
                    }
                            
                    if (chk==false)
                    {
                        $scope.parsedJsonFavCSA.push(angular.fromJson($scope.parsedJsonFavCS2[i]));
                    }
                        
            }
                
                $scope.parsedJsonFavCS=angular.fromJson($scope.parsedJsonFavCSA)
                console.log($scope.parsedJsonFavCS);
        }
    }
    
    
    $scope.removeFromLocalStorage=function (key,id)
    {
        var json = JSON.parse(localStorage[key]);
        console.log("JSON Length Before Delete="+json.length);
        if (key == "Comm"){
            comIdArr=sharedProperties.getStarComProperty()
            deleteStar(comIdArr,id)
        } else if(key=="Legs"){
            legIdArr=sharedProperties.getStarLegProperty()
            deleteStar(legIdArr,id)
            
        } else if(key=="Bills"){
            billIdArr=sharedProperties.getStarBillProperty()
            deleteStar(billIdArr,id)
        }
        
        
        for (i=0;i<json.length;i++)
        {
            if (key == "Legs")
            {
                if (json[i].bioguide_id == id) 
                    json.splice(i,1);
                
            }
            if (key == "Bills")
            {
                console.log("In Bills");
                if (json[i].bill_id == id){
                    console.log("In Bills delting bill_id"+json[i].bill_id);
                    json.splice(i,1);
                }
            }
            if (key=="Comm")
            {
                if (json[i].committee_id == id)
                    json.splice(i,1);
            }
        }
        
            
        localStorage[key] = JSON.stringify(json);
        
            $scope.getFavBills();
            $scope.getFavLegs();
            $scope.getFavComs();

    }    
    
    

    
});