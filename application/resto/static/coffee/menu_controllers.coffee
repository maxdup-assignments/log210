angular.module('resto.menuControllers', [])
.controller 'MenuController', ($scope, $location, $http, $routeParams) ->
  param = $routeParams.param

  $http.get('api/all_resto')
    .success (data) ->
      if param
        $scope.current_resto =
          (resto for resto, resto in data when resto.pk == param)[0]

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
    $http.post('/api/edit_menu', $scope.current_resto)
      .success (data) ->
        console.log(data)