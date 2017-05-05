angular.module('opal.reporting').controller(
    'ReportDetailCtrl', function($rootScope, $scope, report){
      $scope.report = report;
    }
);
