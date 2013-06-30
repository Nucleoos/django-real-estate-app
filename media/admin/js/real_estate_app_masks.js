(function($){
    $(document).ready(function($) {
		$.mask.masks = $.extend($.mask.masks,{
			'money': { mask: '99,999.999.999.999', type: 'reverse',defaultValue: '000'},
			'zip_code': { mask: '99999-999'},
			'decimal': {mask:'99.999999999999',type:'reverse'},
			'area': {mask:'99,999.999.999.999',type:'reverse',defaultValue: '000'},
			'phone':{mask:'(99)9999-9999'},
			'celphone':{mask:'(99)9999-9999'},
			'cpf':{mask:'999.999.999-99'},
			'cnpj':{mask:'99.999.999/9999-99'},
			'rg': { mask: '999.999.999.999.999',type:'reverse'},
		});

		$('input:text').setMask();

		$('#property_form').submit(function() {
			$('input:text').each(function (){
				if ($(this).attr('alt')==='money' || $(this).attr('alt') === 'area') {
					var val =$(this).val();
					$(this).val($.mask.string(val,'decimal'));
				}
			})
		});

		$('td[alt="price"]').each( function () {
			$(this).html('R$ '+$.mask.string($(this).text(),'money'));
		});

	});
})(django.jQuery);
