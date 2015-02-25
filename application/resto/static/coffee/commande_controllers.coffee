angular.module('resto.commandeControllers', ['ui.bootstrap'])
.controller 'CommandeController', ($scope, $http, $routeParams) ->
  param = $routeParams.param

  $scope.order = {
    'details': {
      'commande': [],
      'adresse': '',
      'time': new Date(),
    },
  'restaurant': param
  }

  $http.get('api/profile')
    .success (data) ->
      $scope.profile = data
      $scope.order.details.adresse = $scope.profile.adresse[0]

  $http.get('api/all_resto')
    .success (data) ->
      if param
        $scope.current_resto =
          (resto for resto, resto in data when resto.pk == param)[0]

  $scope.add_item = (item) ->
    if item in $scope.order.details.commande
      item.qty += 1
    else
      item.qty = 1
      $scope.order.details.commande.push(item)

  $scope.remove_item = (item) ->
    $scope.order.details.commande =
      _.without($scope.order.details.commande, item)
  $scope.qty_adjust = (item, adjustment) ->
    item.qty = Math.max(0, item.qty + adjustment)

  $scope.total = ->
    total = 0
    for item in $scope.order.details.commande
      total += item.price * item.qty
    return total

  $scope.place_order = ->
    if $scope.order.details.adresse == '##new'
      $scope.profile.adresse.push($scope.new_address)
      $scope.order.details.adresse = $scope.new_address
      console.log('new profile', $scope.profile)
      $http.post('api/edit_profile', $scope.profile)
        .error (data) ->
          console.log(data)
    $http.post('api/create_commande', $scope.order)
      .success (data) ->
        alert('commande envoyé')
        console.log(data)
      .error (data) ->
        console.log(data)
  $scope.minDate = new Date()
  $scope.hstep = 1
  $scope.mstep = 15

  $scope.open = ($event) ->
    $event.preventDefault()
    $event.stopPropagation()
    $scope.opened = true


.controller 'CommandeManageController', ($scope, $http, $routeParams) ->
  param = $routeParams.param
  $scope.commandes = []
  $http.post('api/resto_commande', param)
    .success (data) ->
      $scope.commandes = data
    .error (data) ->
      console.log(data)

  $scope.update_status = (commande, status) ->
    $http.post('api/update_commande_status', {
      'status': status,
      'commande': commande})
      .success (data) ->
        commande.status = status