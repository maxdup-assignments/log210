angular.module('resto.userControllers', ['resto.dev'])

.controller 'RootController',
($scope, $location, $http, $route, $rootScope, Profile, conf) ->

  $scope.loginform = {
    'username':''
    'password':''
  }
  Profile.get({id:'self'}).$promise.then(
    (value) ->
      $scope.profile = value
      $rootScope.$broadcast('profileload')
  )

  $scope.login = ->
    $http.post(conf.url + 'login', $scope.loginform)
      .success (data) ->
        $scope.auth = true
        $scope.loggingin = false
        $scope.profile = data.profile
        $scope.username = data.username
        $route.reload()

  $scope.logout = ->
    $http.get(conf.url + 'logout')
      .success (data) ->
        $scope.auth = false
        $scope.profile = null
        $scope.loginform['username'] = ''
        $scope.loginform['password'] = ''
        $location.path( "/app/#/home" )
        $route.reload()


.controller 'UserController',
($scope, $location, $http, Profile, Resto) ->

  userform = {
    'user':{
      'username':''
      'email':'',
      'first_name': '',
      'last_name': '',
      'password': ''}
    'date_naissance': '',
    'adresse': '',
    'telephone': '',
  }

  _.extend($scope.userform, userform)

  $scope.submit = (restaurateur=false) ->
    $scope.userform.is_restaurateur = restaurateur
    $scope.userform.user.email = $scope.userform.user.username
    userform = {}
    Profile.save($scope.userform).$promise.then(
      (value) ->
        if $location.path() == '/admin/users'
          $scope.profiles.push(data)
          if $scope.userform.resto
            $scope.options =
              (opt for opt, opt in $scope.options \
                when opt.value != $scope.userform.resto)
            $scope.selected_resto = $scope.options[0]
          else
            alert("il est preferable d'assigner un restaurant")
          _.extend($scope.userform, userform)
        else
          alert('registration successful')
          $location.path("app/#/home"))

  if $location.path() == '/admin/users'

    $scope.profiles = Profile.query()
    $scope.options = [{'label':'None', 'value':''}]
    $scope.selected_resto = $scope.options[0]

    Resto.query().$promise.then(
      (value) ->
        $scope.restos = value
        $scope.available_resto =
          (resto for resto, resto in $scope.restos \
            when resto.user == null)
        for resto in $scope.available_resto
          $scope.options.push({'label':resto.name, 'value':resto.pk}))
 
  $scope.edit = (profile) ->
    profile.backup = _.clone(profile)
    profile.backup.user = _.clone(profile.user)

  $scope.cancel = (profile) ->
    _.extend(profile, profile.backup)
    delete profile['backup']

  $scope.save = (profile) ->
    Profile.update({id:profile.user.pk}, profile).$promise.then(
      (value) ->
        delete profile['backup'])

  $scope.remove = (profile) ->
    Profile.delete(id:profile.user.pk).$promise.then(
      (value) ->
        $scope.profiles = _.without($scope.profiles, profile))
