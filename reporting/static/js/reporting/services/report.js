angular.module('opal.reporting').factory('Report', function($window, $interval, $http){
  "use strict";
  var Report = function(reportDefinition){
    _.extend(this, reportDefinition);
    this.asyncWaiting = false;
    this.asyncReady = false;
  };

  Report.prototype = {
    download: function(){
      if(this.asyncReady){
        $window.open(this.reportFileUrl, '_blank');
      }
      else{
        $window.open(this.download_link, '_blank');
      }
    },
    downloadAsynchronously: function(){
      var self = this;
      this.asyncWaiting = true;
      $http.get(this.download_link).then(function(result){
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
