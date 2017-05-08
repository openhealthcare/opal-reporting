angular.module('opal.reporting').factory('Report', function($window, $interval, $http){
  "use strict";
  var Report = function(reportDefinition){
    _.extend(this, reportDefinition);
    this.asyncWaiting = false;
    this.asyncReady = false;
    this.criteria = {something: "interesting"};
  };

  Report.prototype = {
    download: function(){
      $window.open(this.reportFileUrl, '_blank');
    },
    downloadAsynchronously: function(){
      var self = this;
      this.asyncWaiting = true;
      $http.post(
        this.download_link, {criteria: JSON.stringify(this.criteria)}
      ).then(function(result){
        self.reportStatusUrl = result.data.report_status_url;
        self.reportFileUrl = result.data.report_file_url;
        self.interval = $interval(_.bind(self.getAsyncStatus, self), 2000);
      });
    },
    getAsyncStatus: function(){
      var self = this;
      $http.get(this.reportStatusUrl).then(function(result){
        if(result.data.ready){
          self.asyncReady = true;
          self.asyncWaiting = false;
          $interval.cancel(self.interval);
        }
      });
    }
  };

  return Report;
});
