$(document).ready(
    function(){
        // console.log($);

        var firework_names = [
            "git_basher",
            "gunicorn",
            "ninja_star",
            "python",
            "stack_overflow"
        ];

        // (function($){
        //     $.fn.randomImage = function(img){

        //         var i = Math.floor(Math.random()*firework_names.length);

        //         document.getElementById(img).src = "{% static 'message_app/img/"+ firework_names[i]+ ".png' %}";
        //         return this;
        //     };
        // })(jQuery);
        
        (function($){
            $.fn.randomImage = function(){

                if (document.getElementById("id")){

                }

                var i = Math.floor(Math.random()*firework_names.length);
                this.attr('src', "static/message_app/img/"+ firework_names[i]+ ".png");
                return this;

            };
        })(jQuery);

        // $("#random-firework").randomImage();

    }
);