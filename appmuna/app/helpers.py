from pprint import pprint
from backend import models
from operator import itemgetter
import statistics

  
def randomColor(space) :
    colors = ['#A3E4D7','#76D7C4', '#48C9B0','#1ABC9C', '#17A589', '#148F77','#117864']
    return colors[:space]

def split_list (list_dt,n_length):
    return [list_dt[i:i+n_length] for i in range(0, len(list_dt), n_length)]

def get_table_summarizer(indicator_id, filter_ = []):
    model = models.BackendIndicatorsModel.objects.filter(pk=indicator_id).first()
    model_data = models.BackendContentIndicatorsModel.objects.filter(indicator_id=indicator_id)

    if len(filter_) > 0:
        model_data_ = []
        for dt in filter_:
            year, period_item = dt.split('_')
            qry = model_data.filter(year = year, item_period = period_item)
            if qry.exists():
                model_data_+= qry.values()

        model_data = sorted(model_data_, key=itemgetter('item_row', 'year', 'item_period', 'item_char')) 
    else:
        model_data = model_data.order_by('item_row', 'year', 'item_period', 'item_char').values()

    table_summarize = []
    for dt in model_data:
        items_col =  {
            'item_char_id': dt['item_char'],
            'item_char': models.BackendCharacteristicItemsModel.objects.filter(pk=dt['item_char']).first().item_char if len(dt['item_char']) > 0 else '',
            'values' : [round(float(dt["value"]), model.decimal_point)]
        }

        if len(table_summarize) > 0:
            check_exist = next((index for (index, d) in enumerate(table_summarize) if dt['item_row'] == d['row_id']), None)
            if check_exist is not None:
                check_item = next((index for (index, d) in enumerate(table_summarize[check_exist]['items']) if dt['item_char'] == d['item_char_id']), None)
                if check_item is not None:
                    table_summarize[check_exist]['items'][check_item]['values'].append(round(float(dt["value"]), model.decimal_point))
                else:
                    table_summarize[check_exist]['items'].append(items_col)

                continue

        table_summarize.append({
            'row_id' :  dt["item_row"],
            'row_name' : models.BackendRowsItemsModel.objects.filter(pk = dt["item_row"]).first().item_row if model.row_group_id.row_items.first().order_num != 99 else model.name,
            'items' : [items_col]
        })
    
    for dt_rows in table_summarize:
        for dt_chars in dt_rows['items']:
            values = dt_chars['values']
            dt_chars['stats_items'] = [
                {'stat' : 'Min', 'val' : min(values)},
                {'stat' : 'Median', 'val' : statistics.median(values)},
                {'stat' : 'Average', 'val' : statistics.mean(values)},
                {'stat' : 'Max', 'val' : max(values)},
            ]
    return table_summarize

def get_content_comparison(datalists):
    
    for dt in datalists:

        if len(dt['items']) == 1: # Perbandingan antar triwulan di tahun yang sama
            dt_years = dt['items'][0]
            first_data = dt_years['items'][0]
            second_data = dt_years['items'][1]
            year_comparison = f'{dt_years["year"]}'
        else:
            dt_first_years = dt['items'][0]
            dt_second_years = dt['items'][1]
            
            first_data = dt_first_years['items'][0]
            second_data = dt_second_years['items'][0]
            year_comparison = f'{dt_first_years["year"]}'
            
        cols_comparisons = []
        for idx in range(len(first_data['items'])):
            dev = second_data['items'][idx]['value'] - first_data['items'][idx]['value']
            dev_percent = round(dev / first_data['items'][idx]['value'] * 100, 2) if first_data['items'][idx]['value'] != 0 else '-'
            
            if type(dev_percent) == float:
                
                if dev_percent < 0 :
                    title = 'Penurunan'
                    class_, icon = '', 'mdi-arrow-down-bold text-danger'
                    # class_, icon = 'text-danger', 'mdi-arrow-down-bold'
                else:
                    title = 'Peningkatan'
                    class_, icon = '', 'mdi-arrow-up-bold text-success'
                    # class_, icon = 'text-success', 'mdi-arrow-up-bold'
                
                value = f'{dev_percent}% <span class="mdi {icon}"></span> '
                # value = f'<span class="{class_} me-2"><span class="mdi {icon}"></span>{dev_percent}%</span>'
                content = f'Terjadi {title} sebesar {dev} ({dev_percent}%) dibandingkan dengan data {first_data["item_period"]}, {year_comparison}'
                title = f'Terjadi {title} {dev_percent}%.'
            else:
                class_ = ''
                value = dev_percent
                content = f'Terjadi {title} sebesar {dev} dibandingkan dengan data {first_data["item_period"]}, {year_comparison}'
                title = f'Terjadi {title} sebesar {dev}',

            dt_ = {
                    'item_char' : first_data['items'][idx]['item_char'],
                    'value' :  value,
                    'title' : title,
                    'class_' : class_,
                    'content' :content
            }
            cols_comparisons.append(dt_)

        if len(dt['items']) == 1: # Perbandingan antar triwulan di tahun yang sama
            dt_years['items'].insert(0, {'item_period': f'Perbandingan ({first_data["item_period"]} {dt_years["year"]} - {second_data["item_period"]} {dt_years["year"]})', 'items': cols_comparisons})
        else:
            dt['items'].insert(0, 
                               {'year': f'Perbandingan ({first_data["item_period"]} {dt_first_years["year"]} - {second_data["item_period"]} {dt_second_years["year"]})',
                                'items': [
                                        {
                                        'item_period' : '',
                                        'item_period_id' : '',
                                        'items' : cols_comparisons
                                    }
                                    ]
                                }
                            )
    return datalists

def get_content_table(indicator_id, filter_ = []):

    model = models.BackendIndicatorsModel.objects.filter(pk=indicator_id).first()
    model_data = models.BackendContentIndicatorsModel.objects.filter(indicator_id=indicator_id)

    if len(filter_) > 0:
        model_data_ = []
        for dt in filter_:
            year, period_item = dt.split('_')
            qry = model_data.filter(year = year, item_period = period_item)
            if qry.exists():
                model_data_+= qry.values()

        model_data = sorted(model_data_, key=itemgetter('item_row', 'year', 'item_period', 'item_char')) 
    else:
        model_data = model_data.order_by('item_row', 'year', 'item_period', 'item_char').values()

    data_content_table = []
    for dt in model_data:
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
            'row_name' : models.BackendRowsItemsModel.objects.filter(pk = dt["item_row"]).first().item_row if model.row_group_id.row_items.first().order_num != 99 else model.name,
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

    if summarize_dt != 'none' and model.unit_id.name.lower() != 'persen':
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
    
    if summarize_dt == 'percent' and model.unit_id.name.lower() != 'persen':
        for dt_rows in data_content_table:
            for dt_years in dt_rows['items']:
                for dt_periods in dt_years['items']:
                    total_each_rows = [dt['sum'] for dt in sum_values_rows if f"{dt_years['year']}_{dt_periods['item_period_id']}" == dt['item_period']]
                    total_each_rows = sum(total_each_rows)
                    dt_periods['items'][-1]['value'] = round(dt_periods['items'][-1]['value'] / total_each_rows * 100, 2)

    return data_content_table

def get_list_periods(model_data_period, filter_ = None):
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

def get_chart_data(data, summarize = 'sum', cons_data = False, have_cols = True, have_rows = True):
    # @cons_data_type : Persen atau Indeks
    label_x = []
    data_collections = []

    cons_data_type = False
    if cons_data:
        cons_data_type = True if cons_data in ['persen', 'indeks'] else False

    for dt_content in data:
        list_data = []
        for idx, dt_year in enumerate(dt_content['items']):
            for dt_period in dt_year['items']:
                label = f"{dt_period['item_period']} {dt_year['year']}"
                if label not in label_x:
                    label_x.append(label)

                for idx2, dt_col in enumerate(dt_period['items']):
                    item_char = dt_col['item_char'].lower()
                    if cons_data_type:
                        if have_cols:
                            colors = randomColor(len(dt_period['items']))
                            check_exist = next((index for (index, d) in enumerate(data_collections) if (d['label'] == dt_col['item_char']) and (d['group'] == dt_content['row_name'])), None)
                            if check_exist is not None:
                                data_collections[check_exist]['data'].append(dt_col['value'])
                            else:
                                data_collections.append(
                                {
                                    'label': f"{dt_col['item_char']}",
                                    'data': [dt_col['value']],
                                    'backgroundColor': colors[idx2],
                                    'stack': f"Stack {dt_content['row_name']}",
                                    'barPercentage': 0.9,
                                    'categoryPercentage': 1,
                                    'group' : dt_content['row_name']
                                })
                        else:
                            list_data.append(dt_col['value'])
                    else:
                        if item_char in ['total', 'rerata', 'persen']:
                            list_data.append(dt_col['value'])

        if (cons_data_type and have_cols) is False:
            data_collections.append({
                'label': dt_content['row_name'],
                'data': list_data
            })

    chart_data = {'labels': label_x, 'data' : data_collections}

    if summarize.lower() in ['sum', 'percent'] or (cons_data == 'persen' and have_cols == False) or (cons_data == 'persen' and have_cols and have_rows == False):
        data_pie = []
        if summarize == 'sum':
            total_period = []
            for idx in range(len(label_x)):
                total_period.append(sum(dt['data'][idx] for dt in data_collections))

            for dt in data_collections:
                percent = []
                for idx, dt_ in enumerate(dt['data']):
                    percent.append(round(dt_/total_period[idx]*100, 2))
                dt['data_percent'] = percent

            for idx in range(len(label_x)):
                data_pie.append([dt['data_percent'][idx] for dt in data_collections])
        else:
            for idx in range(len(label_x)):
                data_pie.append([dt['data'][idx] for dt in data_collections])

        chart_data['label_pie_chart'] = [dt['label'] for dt in data_collections]
        chart_data['data_pie'] = data_pie
        chart_data['label_pie_layer'] = [f'Layer {idx+1}: {dt}' for idx, dt in enumerate(label_x)]

        if summarize == 'sum':
            chart_data['agg'] =  'Total'
        elif summarize == 'avg':
            chart_data['agg'] =  'Rerata'
        else:
            chart_data['agg'] =  'Persen (%)'

    return chart_data