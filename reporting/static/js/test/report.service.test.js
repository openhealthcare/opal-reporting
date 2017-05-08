describe('Report', function(){
  "use strict";
var Report, $window, $httpBackend, $interval, $rootScope;


  beforeEach(function(){
    module('opal.reporting');
    inject(function($injector){
      Report = $injector.get('Report');
      $window = $injector.get('$window');
      $httpBackend = $injector.get('$httpBackend');
      $rootScope = $injector.get('$rootScope');
    });

    spyOn($window, "open");
  });

  afterEach(function(){
    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();
  });

  it('should initialise the report', function(){
    var report = new Report({download_link: "some_link"});
    expect(report.download_link).toBe("some_link");
    expect(report.asyncReady).toBe(false);
    expect(report.asyncWaiting).toBe(false);
  });

  it('show open a window on download', function(){
      var report = new Report({download_link: "some_link"});
      report.download();
      expect($window.open).toHaveBeenCalledWith("some_link", '_blank');
  });

  it('should trigger $interval on dowload asynchronously', function(){
    var report = new Report({download_link: "/some_link"});
    $httpBackend.expectGET('/some_link').respond({
      report_status_url: "/reportStats", report_file_url: "/reportFile"
    });
    report.downloadAsynchronously();
    $httpBackend.flush();
    $rootScope.$apply();
    expect(report.asyncWaiting).toBe(true);
    expect(report.reportStatusUrl).toBe("/reportStats");
    expect(report.reportFileUrl).toBe("/reportFile");
    expect(!!report.interval).toBe(true);
  });

  it('should set async=true when the result comes in', function(){
    var report = new Report({download_link: "/some_link"});
    report.reportStatusUrl = "/reportStatus";
    report.asyncWaiting = true;
    $httpBackend.expectGET('/reportStatus').respond({
      ready: true
    });
    report.getAsyncStatus();
    $httpBackend.flush();
    $rootScope.$apply();
    expect(report.asyncWaiting).toBe(false);
    expect(report.asyncReady).toBe(true);
  });

});
