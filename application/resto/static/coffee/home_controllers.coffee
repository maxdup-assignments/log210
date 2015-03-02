angular.module('resto.homeControllers', [])
.controller 'HomeController', ($scope, $http) ->
  $scope.restos = []

  $http.get('api/all_resto')
    .success (data) ->
      $scope.restos = data
