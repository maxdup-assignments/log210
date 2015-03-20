angular.module('resto.homeControllers', [])
.controller 'HomeController', ($scope, $http) ->
  $scope.restos = []

  $http.get('http://127.0.0.1:8000/api/resto')
    .success (data) ->
      $scope.restos = data
