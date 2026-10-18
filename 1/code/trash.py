hermann = hist[hist['station'] == 'Hermannplatz']

sea.set_theme(style='ticks', palette='pastel', font='sans-serif', font_scale=1.2, color_codes=True, rc=None)
sea.barplot(hermann, x='time', y='inspections')
sea.despine()

hist['incident'] = (hist['line'] + ' ' +
                    hist['station'] + ' ' +
                    hist['day'] + ' ' +
                    hist['time'].astype(str))

top100 = hist.nlargest(100, "inspections")

sea.histplot(data=top100, x='incident', y='inspections')

libby.xticks(rotation=90)
libby.show()