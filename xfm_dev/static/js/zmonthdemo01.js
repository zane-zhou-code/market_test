function timeselect(){
   $('.ui.fluid.search.dropdown')
        .dropdown({ fullTextSearch: true });
	
    $('.start_time').calendar({
			type: 'month',//datatime年月日时分  date就是年月日
			ampm: false,//默认会有 上午，下午，或者AM PM，false就会没有默认的PM AM上午下午；文档写的是中文要在text里设置，但是我写的时候本地好好的是英文，但是一上线就成了中文，如 9:00 上午，所以该处设置成了false
			endCalendar: $('.end_time'),//开始时间选好后，会调起结束时间，而且结束时间不会大于开始时间
			text: {
			  days: ['S', 'M', 'T', 'W', 'T', 'F', 'S'],
			  months: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
			  monthsShort: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
			  today: 'Today',
			  now: 'Now',
			  am: 'AM',
			  pm: 'PM'
			},
			popupOptions: {
			  position: 'bottom left',
			  lastResort: 'bottom left',
			  prefer: 'opposite',
			  hideOnScroll: false
			},
			formatter: { // 自定义日期的格式
				date: function(date, settings) {
					if (!date) return '';
					var year  = date.getFullYear();
					var month = date.getMonth() + 1;
					var day   = date.getDate();
					month = month < 10 ? '0'+month : month;
					day   = day   < 10 ? '0'+day : day;
					// return year + '-' + month + '-' + day;//不写时分hours minute也会返回
					return year + '-' + month;//不写时分hours minute也会返回
				}
			}
	});
    $('.end_time').calendar({
            type: 'month',
            ampm: false,
            startCalendar: $('.start_time'),
			text: {
			  days: ['S', 'M', 'T', 'W', 'T', 'F', 'S'],
			  months: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
			  monthsShort: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
			  today: 'Today',
			  now: 'Now',
			  am: 'AM',
			  pm: 'PM'
			},
            formatter: { // 自定义日期的格式
                date: function(date, settings) {
                    if (!date) return '';
                    var year  = date.getFullYear();
                    var month = date.getMonth() + 1;
                    var day   = date.getDate();
                    month = month < 10 ? '0'+month : month;
                    day   = day   < 10 ? '0'+day   : day;
                    return year + '-' + month;
                }
            }
    });
}