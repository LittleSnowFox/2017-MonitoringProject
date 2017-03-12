'use strict';


/**
 * Application monitorApp declaration
 * also includes ngRoute for all our routing needs
 */
var monitorApp = angular.module('monitorApp', [
    // "module" dependances
    //'ui.bootstrap',
    'ngRoute'
]);


/**
 * Configure our routes
 */
monitorApp.config([ '$routeProvider', '$locationProvider', function( $routeProvider, $locationProvider ){
    $routeProvider

        // route for the home page
        .when('/', {
            templateUrl : 'partials/home.html',
            controller  : 'mainController'
        })

        // route for the about page
        .when('/about', {
            templateUrl : 'partials/about.html',
            controller  : 'aboutController'
        });

        $locationProvider.html5Mode({
        enabled: true,
        requireBase: false
        });
}]);


/**
 * Application controller.
 */
monitorApp.controller('mainController', function($scope) {
    // create a message to display in our view
    $scope.message = 'Monitore your web sites at any time !';
});

monitorApp.controller('aboutController', function($scope) {
    $scope.message = 'Look! I am an about page.';
});

//.controller('HeaderCtrl', function($scope, $location) {
//    $scope.$on('$locationChangeSuccess', function(/* EDIT: remove params for jshint */) {
//        var path = $location.path();
//        //EDIT: cope with other path
//        $scope.templateUrl = (path==='/' || path==='/home' || path==='/about') ? 'templates/header.html' : 'templates/header.html' : 'templates/header.html' ;
//    });
//})
