jQuery(document).ready(function ($) {
    $('.field-parent_id').hide();

    $("#id_is_parent_available").change(function () {

        if ($("#id_is_parent_available").val() === 'true') {
            // alert($("#id_organization").val());
            fetch("http://127.0.0.1:8000/document/document_list")
                .then(response => response.json())
                .then(data => {
                    
                    data[0].forEach(element => {
                        console.log("a");
                        
                    });
                    // do something with users data
            }
            
            );
            // $.ajax({                       // initialize an AJAX request
            //     type: "POST",
            //     url: 'knowledgebase/document/document_list',
            //     data: {
            //         'id_organization': $("#id_organization").val(),       // add the country id to the POST parameters                 
            //     },
            //     dataType: 'json',
            //     success: function (data) {  
            //          // `data` is from `get_topics_ajax` view function
            //          alert("OK");
            //         console.log(data);

            //         let html_data = '<option value="">---------</option>';
            //         data.forEach(function (data) {
            //             html_data += `<option value="${data.id}">${data.title}</option>`
            //         });
            //         $("#question-topic").html(html_data); // replace the contents of the topic input with the data that came from the server

            //     }
            // });
            //id: id_parent_id
            //name : parent_id
            $('.field-parent_id').show();

        } else if ($("#id_is_parent_available").val() === 'false') {
            $('.field-parent_id').hide();

        } else if ($("#id_is_parent_available").val() === 'Unknown') {
            alert($('#id_is_parent_available').val());
            $('.field-parent_id').hide();
        }
    });

});