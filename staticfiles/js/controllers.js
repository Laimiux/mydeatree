'use strict';

/* Controllers */

function PhoneListCtrl($scope, $http) {
	$http.get('/phones/phones.json').success(function(data) {
		$scope.phones = data;
	});

	$scope.orderProp = 'age';
}


function PublicIdeaListCtrl($scope, $http) {
	var api_url = PUBLIC_IDEA_API || '/api/v1/public_ideas/';
	$http.get(api_url).success(function(data){
		$scope.meta = data.meta
		$scope.public_ideas = data.objects;
	});
	
	$scope.orderProp = '-modified_date';
}

function PublicIdeaDetailCtrl($scope, $routeParams, $http) {
	var api_url = PUBLIC_IDEA_API || '/api/v1/public_ideas/';
	$http.get(api_url + $routeParams.ideaId).success(function(data) {
		$scope.public_idea = data
	});
}


function PersonalIdeaListCtrl($scope) {
	
}

function PersonalIdeaDetailCtrl($scope) {
	
}

function FavoriteIdeaListCtrl($scope) {
	
}

function FavoriteIdeaDetailCtrl($scope) {
	
}
