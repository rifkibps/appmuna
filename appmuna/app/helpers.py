from pprint import pprint
from backend import models
from operator import itemgetter

def split_list (list_dt,n_length):
    return [list_dt[i:i+n_length] for i in range(0, len(list_dt), n_length)]

def get_content_comparison(datalists):
    
    for dt in datalists:
        for dt_years in dt['items']:
        
            first_data = dt_years['items'][0]['items']
            second_data = dt_years['items'][1]['items']
            cols_comparisons = []

            # pprint(dt_years['items'][0])
            # return

            for idx in range(len(first_data)):
                dev = second_data[idx]['value'] - first_data[idx]['value']
                dev_percent = round(dev / first_data[idx]['value'] * 100, 2) if first_data[idx]['value'] != 0 else '-'
                
                if type(dev_percent) == float:
                    if dev_percent < 0 :
                        title = 'Penurunan', 
                        class_, icon = 'text-danger', 'mdi-arrow-down-bold'
                    else:
                        title = 'Peningkatan'
                        class_, icon = 'text-success', 'mdi-arrow-up-bold'
                    value = f'<span class="{class_} me-2">(<span class="mdi {icon}"></span>{dev_percent}%)</span>'
                    content = f'Terjadi {title} sebesar {dev} ({dev_percent}%) dibandingkan dengan data {dt_years["items"][0]["item_period"]}, {dt_years["year"]}'
                    title = f'Terjadi {title} {dev_percent}%.'
                else:
                    class_ = ''
                    value = dev_percent
                    content = f'Terjadi {title} sebesar {dev} dibandingkan dengan data {dt_years["items"][0]["item_period"]}, {dt_years["year"]}'
                    title = f'Terjadi {title} sebesar {dev}',

                cols_comparisons.append({
                    'item_char' : first_data[idx]['item_char'],
                    'value' :  value,
                    'title' : title,
                    'class_' : class_,
                    'content' :content
                })
                
            dt_years['items'].insert(0, {'item_period': f'Perbandingan ({dt_years["items"][0]["item_period"]} {dt_years["year"]} - {dt_years["items"][1]["item_period"]} {dt_years["year"]})', 'items': cols_comparisons})

    return datalists

def get_content_table(indicator_id, filter_ = None):

    model = models.BackendIndicatorsModel.objects.filter(pk=indicator_id).first()
    model_data = models.BackendContentIndicatorsModel.objects.filter(indicator_id=indicator_id)

    if filter_:
        years = []
        periods_items = []
        for dt in filter_:
            year, period_item = dt.split('_')
            years.append(year)
            periods_items.append(period_item)
        model_data = model_data.filter(year__in = years, item_period__in=periods_items)
    
    data_content_table = []
    for dt in model_data.order_by('item_row', 'year', 'item_period', 'item_char').values():
        items_col = {
            'item_char_id': dt['item_char'],
            'item_char': models.BackendCharacteristicItemsModel.objects.filter(pk=dt['item_char']).first().item_char if len(dt['item_char']) > 0 else '',
            'id_content_field': dt['id'],
            'value' : round(float(dt["value"]), model.decimal_point)
        }
        
        items_period = {
            'item_period_id' : dt["item_period"],
            'item_period' : models.BackendPeriodNameItemsModel.objects.filter(pk=dt["item_period"]).first().item_period,
            'items': [items_col]
        }
        
        if len(data_content_table) > 0:

            check_exist = next((index for (index, d) in enumerate(data_content_table) if dt['item_row'] == d['row_id']), None)
            if check_exist is not None:
                check_year = next((index for (index, d) in enumerate(data_content_table[check_exist]['items']) if dt['year'] == d['year']), None)
                if check_year is not None: # Cek apakah tahun ada di dalam list? Jika Not None, cek ketersedian periode item
                    check_item_period = next((index for (index, d) in enumerate(data_content_table[check_exist]['items'][check_year]['items']) if dt['item_period'] == d['item_period_id']), None)
                    if check_item_period is not None:
                        check_content_field = next((index for (index, d) in enumerate(data_content_table[check_exist]['items'][check_year]['items'][check_item_period]['items']) if dt['item_char'] == d['item_char_id']), None)
                        if check_content_field is None:
                            data_content_table[check_exist]['items'][check_year]['items'][check_item_period]['items'].append(items_col)
                    else:
                        data_content_table[check_exist]['items'][check_year]['items'].append(items_period)
                else:
                    data_content_table[check_exist]['items'].append(
                        {
                            'year' : dt["year"],
                            'items' : [items_period] 
                        }
                    )

                continue

        content_data = {
            'row_id' : dt["item_row"],
            'row_name' : models.BackendRowsItemsModel.objects.filter(pk = dt["item_row"]).first().item_row,
            'order_num' : models.BackendRowsItemsModel.objects.filter(pk = dt["item_row"]).first().order_num,
            'items' : [
                {
                    'year' : dt["year"],
                    'items' : [ items_period] 
                }
            ]
        }

        data_content_table.append(content_data)
    
    data_content_table = sorted(data_content_table, key=itemgetter('order_num'))

    summarize_dt = model.get_summarize_status_display().lower()
    sum_values_rows = []
    if summarize_dt != 'none':
        for dt_rows in data_content_table:
            for dt_years in dt_rows['items']:
                for dt_periods in dt_years['items']:
                    # Add summarize data
                    dt_collections = []
                    for dt_cols in dt_periods['items']:
                        dt_collections.append(float(dt_cols['value']))
                    
                    if summarize_dt == 'sum':
                        smr = sum(dt_collections)
                        item_char = 'Total'
                    elif summarize_dt == 'avg':
                        smr = sum(dt_collections) / len(dt_collections)
                        item_char = 'Rerata'
                    else: # For percent
                        smr = sum(dt_collections)
                        item_char = 'Persen'

                    dt_periods['items'].append({
                        'item_char' : item_char,
                        'value': smr
                    })
                    sum_values_rows.append({'item_period' : f"{dt_years['year']}_{dt_periods['item_period_id']}", 'sum' : sum(dt_collections)})
    
    if summarize_dt == 'percent':
        for dt_rows in data_content_table:
            for dt_years in dt_rows['items']:
                for dt_periods in dt_years['items']:
                    total_each_rows = [dt['sum'] for dt in sum_values_rows if f"{dt_years['year']}_{dt_periods['item_period_id']}" == dt['item_period']]
                    total_each_rows = sum(total_each_rows)
                    dt_periods['items'][-1]['value'] = round(dt_periods['items'][-1]['value'] / total_each_rows * 100, 2)

    return data_content_table

def get_list_periods(model_data_period, filter_ = None, no_cols = False):
    list_periods = []
    list_filter = []

    if filter_:
        for dt in filter_:
            splitter = dt.split('_')
            list_filter.append({'year': splitter[0], 'item_period': splitter[1]})
            
    for dt in model_data_period:
        name = models.BackendPeriodNameItemsModel.objects.filter(pk=dt["item_period"]).first().item_period
        dt_periods = {
            'id' : dt["item_period"],
            'name' : '' if name.lower() == 'tahun' else name,
        }
        
        if filter_:
            check = next((True for dt_ in list_filter if dt_['year'] == dt['year'] and dt_['item_period'] == dt['item_period']), False)
            dt_periods['checked'] = 'checked' if check else ''
        else:
            dt_periods['checked'] = 'checked'

        check_exist = next((index for (index, d) in enumerate(list_periods) if d["year"] == dt['year']), None)
        if check_exist is None:
            list_periods.append({
                "year"    : dt['year'],
                "periods" : [dt_periods]
            })
        else:
            list_periods[check_exist]['periods'].append(dt_periods)

    return list_periods


def get_chart_data(data, summarize = 'sum'):

    label_x_line = []
    data_line = []
    for dt_content in data:
        list_data_line = []
        for dt_year in dt_content['items']:
            for dt_period in dt_year['items']:
                label = f"{dt_period['item_period']} {dt_year['year']}"
                if label not in label_x_line:
                    label_x_line.append(label)

                for dt_col in dt_period['items']:
                    item_char = dt_col['item_char'].lower()
                    if item_char == 'total' or item_char == 'rerata' or item_char == 'persen':
                        list_data_line.append(dt_col['value'])
                        continue

        data_line.append({
            'label': dt_content['row_name'],
            'data': list_data_line
        })

    if summarize.lower() in ['sum', 'percent']:
        data_pie = []
        if summarize == 'sum':
            total_period = []
            for idx in range(len(label_x_line)):
                total_period.append(sum(dt['data'][idx] for dt in data_line))

            for dt in data_line:
                percent = []
                for idx, dt_ in enumerate(dt['data']):
                    percent.append(round(dt_/total_period[idx]*100, 2))
                dt['data_percent'] = percent

            for idx in range(len(label_x_line)):
                data_pie.append([dt['data_percent'][idx] for dt in data_line])
        else:
            for idx in range(len(label_x_line)):
                data_pie.append([dt['data'][idx] for dt in data_line])

    chart_data = {'labels': label_x_line, 'data' : data_line}

    if summarize == 'sum':
        chart_data['agg'] =  'Total'
    elif summarize == 'avg':
        chart_data['agg'] =  'Rerata'
    else:
        chart_data['agg'] =  'Persen (%)'

    if summarize.lower() in ['sum', 'percent']:
        chart_data['label_pie_chart'] = [dt['label'] for dt in data_line]
        chart_data['data_pie'] = data_pie
        chart_data['label_pie_layer'] = [f'Layer {idx+1}: {dt}' for idx, dt in enumerate(label_x_line)]
    
    return chart_data