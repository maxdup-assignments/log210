angular.module('restoApp', ['ngRoute', 'ngCookies', 'ngResource', 'resto.services', 'resto.userControllers', 'resto.restoControllers', 'resto.menuControllers', 'resto.homeControllers', 'resto.commandeControllers', 'gettext'])
.config ($routeProvider, $httpProvider) ->
  $routeProvider
  .when '/home',
    controller: 'HomeController'
    templateUrl: 'partials/home.html'
  .when '/register',
    controller: 'UserController',
    templateUrl: 'partials/register.html'
  .when '/profile',
    controller: 'UserController',
    templateUrl: 'partials/profile.html'
  .when '/admin/users',
    controller: 'UserController',
    templateUrl: 'partials/admin_users.html'
  .when '/admin/resto',
    controller: 'RestaurantController',
    templateUrl: 'partials/admin_resto.html'
  .when '/manage_menu/:param',
    controller: 'MenuController',
    templateUrl: 'partials/manage_menu.html'
  .when '/manage/resto',
    controller: 'RestaurantController',
    templateUrl: 'partials/manage_resto.html'
  .when '/resto/:param',
    controller: 'CommandeController',
    templateUrl: 'partials/commande.html'
  .when '/manage_commande/:param',
    controller: 'CommandeManageController',
    templateUrl: 'partials/manage_commande.html'
  .when '/commande/:param',
    controller: 'CommandeConfirmController',
    templateUrl: 'partials/commande_success.html'
  .when '/deliver_commande',
    controller: 'CommandeManageController',
    templateUrl: 'partials/deliver_commande.html'

  .otherwise
    redirectTo: '/home'

  $httpProvider.defaults.xsrfCookieName = 'csrftoken'
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
  $httpProvider.defaults.withCredentials = true

.run (gettextCatalog, $http, $cookies) ->
  $http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken']
  $http.defaults.headers.put['X-CSRFToken'] = $cookies['csrftoken']
  $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken']
  gettextCatalog.setCurrentLanguage('en')
  gettextCatalog.debug = true