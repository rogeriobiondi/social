angular.module('myApp.services', [])

.factory('data', [ '$http', function($http) {
  return {
    getData : function() {
      var url = "http://" + window.location.hostname + ":8000/api";
      return $http.get(url);
    }
  };
}]);
