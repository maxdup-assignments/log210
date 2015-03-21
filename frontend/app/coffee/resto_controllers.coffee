angular.module('resto.restoControllers', [])

.controller 'HomeController', ($scope, $http, Resto) ->
    $scope.restos = Resto.query()

.controller 'RestaurantController',
($scope, $location, $http, Profile, Resto) ->

  $scope.restos = []

  if $location.path() == '/admin/resto'
    $scope.new_resto = {
      'name': '',
      'menu': {},
      'user': '',
    }

    $scope.options = [{'label':'None', 'value':''}]

    $scope.selected_staff = ''
    Profile.query({restaurateur:true}).$promise.then(
      (value) ->
        for profile in value
          $scope.options.push(
            {'label': profile.user.email, 'value': profile.user.pk})
        $scope.selected_staff = $scope.options[0]
        $scope.new_resto.user = $scope.selected_staff.value)

    assign_selection = (resto) ->
      if resto.user
        resto.new_user = option for option in $scope.options \
        when option.value == resto.user.pk
      else
        resto.new_user = $scope.options[0]

    Resto.query().$promise.then(
      (value) ->
        $scope.restos = value
        for resto in $scope.restos
          assign_selection(resto))

    $scope.create_resto = ->
      if not $scope.new_resto.user
        alert("il est préferable d'assigner un restaurateur")

      Resto.save($scope.new_resto).$promise.then(
        (value) ->
          assign_selection(value)
          $scope.restos.push(value)
          $scope.new_resto = {'name':'', 'menu':{}, 'user':''})

  else
    $scope.$on 'profileload', ->
      $scope.restos = Resto.query({user:$scope.profile.user.pk})

  $scope.edit_resto = (resto) ->
    resto.backup = _.clone(resto)
    resto.backup.user = _.clone(resto.user)
    if assign_selection
      assign_selection(resto)

  $scope.save_resto = (resto) ->
    if (resto.user and resto.new_user and resto.new_user.value == resto.user.pk)
      delete resto['new_user']
    delete resto['backup']

    Resto.update({id:resto.pk}, resto).$promise.then(
      (value) ->
        _.extend(resto, value)
        if not value.user
          alert("il est préferable d'assigner un restaurateur"))

  $scope.cancel_resto = (resto) ->
    _.extend(resto, resto.backup)
    delete resto['backup']
    delete resto['new_user']

  $scope.delete_resto = (resto) ->
    Resto.delete({id:resto.pk}).$promise.then(
      (value) ->
        $scope.restos = _.without($scope.restos, resto))