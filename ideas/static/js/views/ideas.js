var app = app || {};

$(function() {
	app.IdeaView = Backbone.View.extend({
		tagName : 'div',
		className : 'well',
		
		
		events: {
			'click .newChildrenIdea' : 'toggleNewIdea',
			'click .editIdea' : 'edit',
			'click .deleteIdea' : 'clear',
			'click .toggleToParent' : 'toggleParent',
		},
		
		initialize: function() {
			//this.model.on( 'change', this.render, this );
			this.model.on( 'destroy', this.remove, this );
			//this.model.on( 'visible', this.toggleVisible, this );	
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
		
		
		
		clear: function() {
			this.model.destroy();	
		},
		
		toggleParent: function() {


			this.model.trigger('parent-change', { parent : this.model.get('id') })
			
			
			var template = Handlebars.compile($('#private_header_idea_template').html());
			$('#idea_header').html(template(this.model.toJSON()));
		},
		
		
		
		
	});
});
