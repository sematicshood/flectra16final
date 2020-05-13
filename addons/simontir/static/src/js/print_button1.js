flectra.define('print_lapharian.print_button1', function (require) {
    "user strict";

    var form_widget = require('web.FormRenderer');
    var core = require('web.core');

    form_widget.include({
        _addOnClickAction: function ($el, node) {
            var self = this;

            $el.click(function () {
                if (node.attrs.custom === "print_lapharian") {
                    var url = "http://localhost/dotmatrix/";

                    if (node.attrs.custom === "print_lapharian") {
                        url = url + "print.php";
                    }
                    console.log(url)

                    var printer_printLap = self.state.data.printLap;
                    if (!printer_printLap) {
                        alert('No data to print. Please click update Printer Data');
                        return;
                    }
                    console.log(printer_printLap)

                    $.ajax({
                        method: "POST",
                        url: url,
                        data: {
                            printer_printLap: printer_printLap
                        },
                        success: function (data) {
                            console.log('success')
                            console.log(data)
                        },
                        error: function (data) {
                            console.log('Failed');
                            console.log(data);
                        }
                    });
                } else {
                    self.trigger_up('button_clicked', {
                        attrs: node.attrs,
                        record: self.state,
                    });
                }
            });
        }
    });
});