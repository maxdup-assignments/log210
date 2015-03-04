angular.module('resto.commandeControllers', ['ui.bootstrap'])
.controller 'CommandeController', ($scope, $http, $routeParams) ->
  param = $routeParams.param

  $scope.order = {
    'details': {
      'commande': [],
      'addressTo': '',
      'addressFrom': '',
      'requestedTime': new Date(),
    },
  'restaurant': param
  }

  $http.get('api/profile')
    .success (data) ->
      $scope.profile = data
      $scope.order.details.addressTo = $scope.profile.adresse[0]

  $http.get('api/all_resto')
    .success (data) ->
      if param
        $scope.current_resto =
          (resto for resto, resto in data when resto.pk == param)[0]
        $scope.order.details.addressFrom = $scope.current_resto.address

  $scope.add_item = (item) ->
    if item in $scope.order.details.commande
      item.qty += 1
    else
      item.qty = 1
      $scope.order.details.commande.push(item)
    update_total()

  $scope.remove_item = (item) ->
    $scope.order.details.commande =
      _.without($scope.order.details.commande, item)
    update_total()

  $scope.qty_adjust = (item, adjustment) ->
    item.qty = Math.max(0, item.qty + adjustment)
    update_total()

  update_total = ->
    $scope.total = 0
    for item in $scope.order.details.commande
      $scope.total += item.price * item.qty

  $scope.place_order = ->
    if $scope.order.details.addressTo == '##new'
      $scope.profile.adresse.push($scope.new_address)
      $scope.order.details.addressTo = $scope.new_address
      $http.post('api/edit_profile', $scope.profile)
        .error (data) ->
          console.log(data)
    $http.post('api/create_commande', $scope.order)
      .success (data) ->
        alert('commande envoyé')
      .error (data) ->
        console.log(data)
  $scope.minDate = new Date()
  $scope.hstep = 1
  $scope.mstep = 15

  $scope.open = ($event) ->
    $event.preventDefault()
    $event.stopPropagation()
    $scope.opened = true


.controller 'CommandeManageController', ($scope, $http, $location, $routeParams) ->
  param = $routeParams.param

  $scope.filtered = (array, filter) ->
    return (name for name in array when filter.indexOf(name.status) != -1)

  if $location.path() == '/deliver_commande'
    directionsService = new google.maps.DirectionsService()
    directionsDisplay = new google.maps.DirectionsRenderer()

    get_route = ->
      request = {
        origin: $scope.current_location or $scope.selected_commande.details.addressFrom,
        waypoints: [
          location:$scope.selected_commande.details.addressFrom,
          stopover:true,
        ],
        destination: $scope.selected_commande.details.addressTo,
        travelMode: google.maps.TravelMode.DRIVING
      }

      directionsService.route(request, (response, status) ->
        if status == google.maps.DirectionsStatus.OK
          directionsDisplay.setDirections(response))

      map = new google.maps.Map(document.getElementById('map-canvas'))
      directionsDisplay.setMap(map)

    $scope.set_selected = (commande) ->
      $scope.selected_commande = commande
      if $scope.selected_commande
        get_route()

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
        commande.details = data.details
        commande.status = data.status
        if 'error' in _.keys(data)
          alert('Un autre livreur a déjà livré cette commande')
      .error (data) ->
        console.log(data)