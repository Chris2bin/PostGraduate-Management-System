(function($) {
    $(function() {
        var userType = $('#id_user_type'),
            fees = $('#id_user_feesOwed');

        function toggleFees(value) {
            value == 0 ? fees.show() : fees.hide();
        }

        // show/hide on load based on pervious value of selectField
        toggleFees(userType.val());

        // show/hide on change
        userType.change(function() {
            toggleFees($(this).val());
        });
    });
})(django.jQuery);