angular.module('resto.restoControllers', [])
.controller 'RestaurantController', ($scope, $location, $http, $routeParams) ->

  param = $routeParams.param

  $scope.restos = []
  $scope.new_resto = {
    'name': '',
    'menu': {},
    'user': '',
  }

  $scope.options = [{'label':'None', 'value':''}]

  $scope.selected_staff = ''
  $http.get('/api/all_staff')
    .success (data) ->
      for user in data
        $scope.options.push({'label': user.email,'value':user.pk})
      $scope.selected_staff = $scope.options[0]
      $scope.new_resto.user = $scope.selected_staff.value

  assign_selection = (resto) ->
    if resto.user
      resto.new_user = option for option in $scope.options \
      when option.value == resto.user.pk
    else
      resto.new_user = $scope.options[0]

  $http.get('/api/all_resto')
    .success (data) ->
      $scope.restos = data
      for resto in $scope.restos
          assign_selection(resto)
      if param
        $scope.current_resto =
          (resto for resto, resto in $scope.restos when resto.pk == param)[0]
        console.log($scope.current_resto)
    .error (data) ->
      console.log(data)

  $scope.create_resto = ->
    $http.post('/api/create_resto', $scope.new_resto)
      .success (data) ->
        assign_selection(data)
        $scope.restos.push(data)
        $scope.new_resto = {'name':'', 'menu':{}, 'user':''}
        alert("il est préferable d'assigner un restaurateur")
      .error (data) ->
        console.log(data)

  $scope.edit_resto = (resto) ->
    resto.backup = _.clone(resto)
    resto.backup.user = _.clone(resto.user)
    assign_selection(resto)

  $scope.save_resto = (resto) ->
    if (resto.user and resto.new_user.value == resto.user.pk)
      delete resto['new_user']
    delete resto['backup']
    $http.post('/api/edit_resto', resto)
      .success (data) ->
        _.extend(resto, data)
        if not data.user
          alert("il est préferable d'assigner un restaurateur")
      .error (data) ->
        console.log(data)

  $scope.cancel_resto = (resto) ->
    _.extend(resto, resto.backup)
    delete resto['backup']
    delete resto['new_user']

  $scope.delete_resto = (resto) ->
    $http.post('/api/delete_resto', resto)
      .success (data) ->
        $scope.restos = _.without($scope.restos, resto)
      .error (data) ->
        console.log(data)
