angular.module('resto.restoControllers', [])
.controller 'RestaurantController', ($scope, $location, $http) ->

  $scope.restos = []

  if $location.path() == '/admin/resto'
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
      .error (data) ->
        console.log(data)

    $scope.create_resto = ->
      if not $scope.new_resto.user
        alert("il est préferable d'assigner un restaurateur")

      $http.post('/api/create_resto', $scope.new_resto)
        .success (data) ->
          assign_selection(data)
          $scope.restos.push(data)
          $scope.new_resto = {'name':'', 'menu':{}, 'user':''}
        .error (data) ->
          console.log(data)

  else
    $http.get('/api/assigned_resto')
      .success (data) ->
        $scope.restos = data
      .error (data) ->
        console.log(data)

  $scope.edit_resto = (resto) ->
    resto.backup = _.clone(resto)
    resto.backup.user = _.clone(resto.user)
    if assign_selection
      assign_selection(resto)
    console.log(resto)

  $scope.save_resto = (resto) ->
    if (resto.user and resto.new_user and resto.new_user.value == resto.user.pk)
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

  $scope.add_menu = () ->
    if not($scope.current_resto.menu.hasOwnProperty('sous_menus'))
      $scope.current_resto.menu.sous_menus = []
    if $scope.new_menu_name
      $scope.current_resto.menu.sous_menus.push({
        'name': $scope.new_menu_name,
        'items':[]
      })
    else
      alert('Le menu doit avoir un nom')
    $scope.new_menu_name = ''

  $scope.add_menuitem = (menu) ->
    if menu.hasOwnProperty('newitem') and menu.newitem.name and menu.newitem.price
      menu.items.push(menu.newitem)
      if not menu.newitem.desc
        alert("il est préférable d'avoir une description")
      menu.newitem = {'name':'', 'desc':'', 'price':''}
    else
      alert('il faut spécifier un nom et un prix')

  $scope.save_menu = ->
    $http.post('/api/edit_resto', $scope.current_resto)
      .success (data) ->
        console.log(data)