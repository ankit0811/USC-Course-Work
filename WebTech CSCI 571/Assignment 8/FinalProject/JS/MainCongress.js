
$(document).ready(function(){
$("#menu-toggle-2").click(function(e){
        e.preventDefault();
        $("#canvas").toggleClass("toggled");
    });
    //getLagislatorDetails();    
});


var app = angular.module('myApp', ['angularUtils.directives.dirPagination']);
app.controller('Legislator', function($scope, $http) {
    $http.get("https://congress.api.sunlightfoundation.com/legislators?apikey=9333ff0e107c475da428e3df914716ef&per_page=all")
    .then(function(response) {
    $scope.selectedData = response.data;
    $scope.SelectedName = 'Legislator';
    $scope.parsedJson=angular.fromJson($scope.selectedData.results);
    $scope.valueHouse='house'
    $scope.valueSenate='senate'
    console.log($scope.parsedJson);
    });
});




app.controller('Bills', function($scope, $http) {
    
    $http.get("https://congress.api.sunlightfoundation.com/legislators?apikey=9333ff0e107c475da428e3df914716ef&per_page=all")
    .then(function(response) {
    $scope.myWelcome = response.data;
    $scope.SelectedName = 'Bills';
    
    });


});


