var app = app || {};

$(function() {
	app.IdeaView = Backbone.View.extend({
		tagName : 'div',
		className : 'well',
		
		events: {
			'click .newChildrenIdea' : 'toggleNewIdea',
			'click .editIdea' : 'edit',
			'click .deleteIdea' : 'remove',
			'click .toggleToParent' : 'toggleToParent',
		},

		render : function() {
			// Compile the template using Handlebars
			var template = Handlebars.compile($("#private_idea_template").html());
		
						
			$(this.el).html(template(this.model.toJSON()));
			// + " " + this.model.text + " created on " + this.model.created_date);
			return this;
		},
		
		toggleNewIdea: function() {
			alert(this.model.id)
		},
		
		edit: function() {
			
		},
		
		remove: function() {
			
		},
		
		toggleToParent: function() {
			this.model.toggleToParent();	
		},
		
		
	});
});
