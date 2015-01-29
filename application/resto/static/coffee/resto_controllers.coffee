angular.module('resto.restoControllers', [])
.controller('RestaurantController', ($scope, $location, $http) ->

  $("[data-toggle=popover]").popover();

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
      console.log(data)
      for resto in $scope.restos
          assign_selection(resto)
      console.log($scope.restos)
    .error (data) ->
      console.log(data)

  $scope.create_resto = ->
    $http.post('/api/create_resto', $scope.new_resto)
      .success (data) ->
        assign_selection(data)
        console.log($scope.restos)
        $scope.restos.push(data)
        $scope.new_resto = {'name':'', 'menu':{}, 'user':''}

      .error (data) ->
        console.log(data)

  $scope.edit_resto = (resto) ->
    resto.backup = _.clone(resto)
    resto.backup.user = _.clone(resto.user)

  $scope.save_resto = (resto) ->
    console.log('sent', resto)
    if (resto.user and resto.new_user.value == resto.user.pk)
      delete resto['new_user']
    delete resto['backup']
    $http.post('/api/edit_resto', resto)
      .success (data) ->
        _.extend(resto, data)
        assign_selection(resto)
        if not data.user
          alert("il est préferable d'assigner un restaurateur")
        console.log(resto)
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
        console.log(data)
      .error (data) ->
        console.log(data)
)