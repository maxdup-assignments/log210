angular.module('resto.homeControllers', [])
.controller 'HomeController', ($scope, $http, Resto) ->
  $scope.restos = Resto.query()
