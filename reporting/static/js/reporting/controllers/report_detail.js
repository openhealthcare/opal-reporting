angular.module('opal.controllers').controller(
    'ReportDetailCtrl', function($scope, Report, reportDefinition){
      $scope.reports = {}
      $scope.startDownload = function(criteria){
        var report = new Report(
          reportDefinition, criteria
        );
        report.startAsynchronousTask();
        $scope.reports[JSON.stringify(criteria)] = report
      }

      $scope.getReport = function(criteria){
        return $scope.reports[JSON.stringify(criteria)];
      }
    }
);
