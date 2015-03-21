angular.module('resto.commandeControllers', ['ui.bootstrap'])

.controller 'CommandeController',
($scope, $http, $routeParams, Resto, Commande) ->
  $scope.form = {}
  param = $routeParams.param

  $scope.order = {
    'details': {
      'commande': [],
      'addressTo': '',
      'addressFrom': '',
      'requestedTime': new Date(),
    },
  'resto': param
  }

  Resto.query().$promise.then(
    (value) ->
      $scope.current_resto =
        (resto for resto, resto in value when resto.pk == param)[0]
      $scope.order.details.addressFrom = $scope.current_resto.address)

  $scope.add_item = (item) ->
    if not $scope.order.details.addressTo
      $scope.order.details.addressTo = $scope.profile.adresse[0]
    if $scope.sending
      $scope.order.details.commande = []
    $scope.sending = false
    $scope.confirm = null
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
    item.qty = Math.max(1, item.qty + adjustment)
    update_total()

  update_total = ->
    $scope.total = 0
    for item in $scope.order.details.commande
      $scope.total += item.price * item.qty

  $scope.place_order = ->
    $scope.sending = true
    if $scope.order.details.addressTo == '##new'
      $scope.profile.adresse.push($scope.new_address)
      $scope.order.details.addressTo = $scope.new_address
      $http.post('http://127.0.0.1:8000/api/edit_profile', $scope.profile)
    Commande.save($scope.order).$promise.then(
      (value) ->
        $scope.confirm = value
        console.log(value)
      (error) ->
        console.log(error.data)
    )

    if $scope.auth == false
      alert('Veuillez vous connecter')


  $scope.minDate = new Date()
  $scope.hstep = 1
  $scope.mstep = 15

  $scope.open = ($event) ->
    $event.preventDefault()
    $event.stopPropagation()
    $scope.opened = true


.controller 'CommandeManageController',
($scope, $http, $location, $routeParams, Commande) ->
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

  $scope.commandes = Commande.query({resto:param})

  $scope.update_status = (commande, status) ->
    updated_commande = commande
    updated_commande.status = status
    if status = 'delivered'
      updated_commande.details.deliveryTime = new Date()
    Commande.update({id:commande.pk}, updated_commande).$promise.then(
      (value) ->
        if 'error' in _.keys(value)
          alert('Un autre livreur a déjà livré cette commande')
        else
          commande = value
      (error) ->
        console.log(error.data))


.controller 'CommandeConfirmController',
($scope, $http, $routeParams, Commande) ->

  param = $routeParams.param
  $scope.total = 0
  Commande.get({id:param}).$promise.then(
    (value) ->
      console.log(value)
      for item in value.details.commande
        $scope.total += item.price * item.qty

      if value.status == 'pending'
        value.status = 'paid'
        Commande.update({id:param}, value).$promise.then(
          (value) ->
            console.log('okay',value)
          (error) ->
            console.log(error.data)
        )
      $scope.confirm = value

    (error) ->
      console.log(error.data)
  )