angular.module('resto.commandeControllers', [])
.controller 'CommandeController', ($scope, $http, $routeParams) ->
  param = $routeParams.param
  $scope.commande = []

  $http.get('api/all_resto')
    .success (data) ->
      if param
        $scope.current_resto =
          (resto for resto, resto in data when resto.pk == param)[0]

  $scope.add_item = (item) ->
    if item in $scope.commande
      item.qty += 1
    else
      item.qty = 1
      $scope.commande.push(item)
    console.log($scope.commande)

  $scope.remove_item = (item) ->
    $scope.commande = _.without($scope.commande, item)
  $scope.qty_adjust = (item, adjustment) ->
    item.qty = Math.max(0, item.qty + adjustment)

  $scope.total = ->
    total = 0
    for item in $scope.commande
      total += item.price * item.qty
    return total

  $scope.order = ->
    order = {
      'details': {
        'commande': $scope.commande,
        'addresse': "",
      },
      'restaurant': param}

    $http.post('api/create_commande', order)
      .success (data) ->
        alert('commande envoyé')
        console.log(data)
      .error (data) ->
        console.log(data)

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