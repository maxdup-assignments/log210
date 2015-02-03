(function() {
  angular.module('resto.directives', []).directive('ngMenueditor', function() {
    return {
      restrict: 'E',
      scope: false,
      templateUrl: '/static/partials/widgets/menu.html'
    };
  });

}).call(this);
