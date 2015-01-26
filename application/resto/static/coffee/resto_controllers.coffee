angular.module('resto.restoControllers', [])
.controller('RestaurantController', ($scope, $location, $http) ->

  $scope.restos = []

  $http.get('/api/all_resto')
    .success (data) ->
      $scope.restos = data
      console.log(data)
    .error (data) ->
      console.log(data)

  $scope.options = []
  $scope.selected_staff = ''
  $http.get('/api/all_staff')
    .success (data) ->
      for user in data
        $scope.options.push({'label': user.email, 'value':user.pk})
    
  $scope.new_resto = {
    'name': '',
    'menu': {},
    'user': $scope.selected_staff,
  }

  $scope.create_resto = ->
    console.log($scope.new_resto)
    $http.post('/api/create_resto', $scope.new_resto)
      .success (data) ->
        $scope.restos.push(data)
        $scope.new_resto = {'name':'', 'menu':{}, 'user':$scope.selected_staff.value}
        console.log($scope.restos)
      .error (data) ->
        console.log(data)

  $scope.delete_resto = (resto) ->
    $http.post('/api/delete_resto', resto)
      .success (data) ->
        $scope.restos = _.without($scope.restos, resto)
        console.log(data)
      .error (data) ->
        console.log(data)
)