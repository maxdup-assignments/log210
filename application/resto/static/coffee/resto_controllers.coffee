angular.module('resto.restoControllers', [])
.controller('RestaurantController', ($scope, $location, $http) ->

  $scope.restos = []

  $http.get('/api/all_resto')
    .success (data) ->
      $scope.restos = data
      console.log(data)
    .error (data) ->
      console.log(data)

  $scope.new_resto = {
    'name': '',
    'menu': {},
    'user': '',
  }

  $scope.options = []
  $scope.selected_staff = ''
  $http.get('/api/all_staff')
    .success (data) ->
      for user in data
        $scope.options.push({'label': user.email, 'value':user.pk})
      $scope.selected_staff = $scope.options[0]
      $scope.new_resto.user = $scope.selected_staff.value

  $scope.create_resto = ->
    $http.post('/api/create_resto', $scope.new_resto)
      .success (data) ->
        $scope.restos.push(data)
        $scope.new_resto = {'name':'', 'menu':{}, 'user':$scope.selected_staff.value}
      .error (data) ->
        console.log(data)

  $scope.edit_resto = (resto) ->
    resto.backup = _.clone(resto)
    resto.backup.user = _.clone(resto.user)
    # todo select correct user
    resto.new_user = $scope.options[0]

  $scope.save_resto = (resto) ->
    console.log(resto.new_user.value, resto.user.pk)
    if (resto.new_user.value == resto.user.pk)
      delete resto['new_user']
    delete resto['backup']
    $http.post('/api/edit_resto', resto)
      .success (data) ->
        console.log(data)

  $scope.cancel_resto = (resto) ->
    _.extend(resto, resto.backup)
    delete resto['backup']
    delete resto['new_user']

  $scope.delete_resto = (resto) ->
    $http.post('/api/delete_resto', resto)
      .success (data) ->
        $scope.restos = _.without($scope.restos, resto)
        console.log(data)
      .error (data) ->
        console.log(data)
)