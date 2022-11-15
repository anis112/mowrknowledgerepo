jQuery(document).ready(function ($) {
    $('.field-parent_id').hide();

    $("#id_is_parent_available").change(function () {


        if ($("#id_is_parent_available").val() === 'true') {
            var base_url = window.location.origin;
            var org_id=($("#id_organization").val());
            fetch(base_url+"/document/document_list/"+org_id, {
                headers:{
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
                },
            })
            .then(response => {
                return response.json() //Convert response to JSON
            })
            .then(data => {
                //Perform actions with the response data from the view
            var form_parent_id=$('#id_parent_id');   
            var option="" ;   
            data.data.forEach(d => {
                //console.log(d.id);
                option+='<option value="'+d.id+'">'+d.title+'</option>'

                
            });  
            //console.log('<select name="parent_id" required="" id="id_parent_id" data-select2-id="select2-data-id_access_category" tabindex="-1" class="select2-hidden-accessible" aria-hidden="true">'+option+'</select>'); 
            $('#id_parent_id').append('<select name="parent_id" required="" id="id_parent_id" data-select2-id="select2-data-id_parent_id" tabindex="-1" class="select2-hidden-accessible" aria-hidden="true">'+option+'</select>');               
            })

            $('.field-parent_id').show();

        } else if ($("#id_is_parent_available").val() === 'false') {
            $('.field-parent_id').hide();

        } else if ($("#id_is_parent_available").val() === 'Unknown') {
            alert($('#id_is_parent_available').val());
            $('.field-parent_id').hide();
        }
    });

});