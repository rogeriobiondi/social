'use strict';

angular.module('myApp.twitter', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/twitter', {
    templateUrl: 'twitter/twitter.html',
    controller: 'TwitterCtrl'
  });
}])

.controller('TwitterCtrl', ['$scope', 'data', function($scope, data) {
  console.log('### TwitterCtrl');
  data.getData().then(
    function(response) {
      $scope.dados = response.data;
      // console.log($scope.dados);
    },
    function(result) {
      console.log("The request failed: ");
      // console.log(result);
    }
  );
}]);
