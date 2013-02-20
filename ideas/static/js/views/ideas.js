var app = app || {};

$(function() {
	app.IdeaView = Backbone.View.extend({
		tagName : 'div',
		className : 'well well-small',
		
		
		events: {
			'click .newChildrenIdea' : 'toggleNewIdea',
			'click .editIdea' : 'edit',
			'click .deleteIdea' : 'clear',
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
			$('#id_parent').val(this.model.id)
			console.log($('#id_parent').val())
			$('#IdeaModal').modal('show');
			
			return false;
		},
		
		edit: function() {
			$('#id_parent').val(this.model.get('parent'))
			$('#id_title').val(this.model.get('title'));
			$('#id_text').val(this.model.get('text'));
			$('#id_idea_pk').val(this.model.id);
			
			if (this.model.get('public')) {
				$('#id_public').attr('checked', true);
			}
			
			console.log(this.model.get('id'))
			$("#IdeaModal").modal('show');
			
			return false;		
		},
		
		
		
		clear: function() {
			if(confirmDelete()) {
				this.model.destroy();
			}
			return false;	
		},
				
	});
});
