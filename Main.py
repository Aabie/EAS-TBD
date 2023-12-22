import pyodbc
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


st.set_page_config(page_title="Database Akademik", page_icon="📚", layout="wide")

connection = pyodbc.connect('Driver={SQL Server};Server=Pongo;Database=Source;Trusted_Connection=yes;')
cursor = connection.cursor()

connection1 = pyodbc.connect('Driver={SQL Server};Server=Pongo;Database=Stagging;Trusted_Connection=yes;')
cursor1 = connection1.cursor()

connection2 = pyodbc.connect('Driver={SQL Server};Server=Pongo;Database=Warehouse;Trusted_Connection=yes;')
cursor2 = connection2.cursor()
#connection.close()
selected_tab = st.sidebar.selectbox("Select a tab:", ["Source", "Stagging", "Warehouse"])

if selected_tab == "Source":
    database = st.selectbox("Pilih tabel source yang ingin ditampilkan:", ("Coin", "Time", "Company", "Coin Value" , "Stock Company"))

    if database == 'Coin':
        cursor.execute("SELECT * FROM Coin")
        data = cursor.fetchall()
        if data:
            # Split and extract the elements from the tuple strings
            formatted_data = [(row[0], row[1], row[2], row[3]) for row in data]

            # Create a DataFrame from the formatted data
            df = pd.DataFrame(formatted_data, columns=['keyCoin','abbrevCoin', 'nameCoin', 'symbolCoin'])

            # Display the DataFrame using Streamlit
            st.dataframe(df, use_container_width=True, hide_index = True)
        else:
            st.error("Tidak ada data yang tersedia.")

    elif database == 'Time':
        cursor.execute("SELECT * FROM Time")
        data = cursor.fetchall()
        if data:
            # Split and extract the elements from the tuple strings
            formatted_data = [(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],row[8], row[9], row[10], row[11], row[12]) for row in data]

            # Create a DataFrame from the formatted data
            df = pd.DataFrame(formatted_data, columns=['keyTime' ,'datetime' ,'dayTime' ,'dayWeekTime' ,'dayWeekAbbrevTime' ,'dayWeekCompleteTime' ,'monthTime' ,'monthAbbrevTime' ,'monthCompleteTime' ,'bimonthTime' ,'quarterTime' ,'semesterTime' ,'yearTime'])

            # Display the DataFrame using Streamlit
            st.dataframe(df, use_container_width=True, hide_index = True)
        else:
            st.error("Tidak ada data yang tersedia.")

    elif database == 'Company':
        cursor.execute("SELECT * FROM Company")
        data = cursor.fetchall()
        if data:
            # Split and extract the elements from the tuple strings
            formatted_data = [(row[0], row[1], row[2], row[3], row[4], row[5]) for row in data]

            # Create a DataFrame from the formatted data
            df = pd.DataFrame(formatted_data, columns=['keyCompany' ,'stockCodeCompany' ,'nameCompany' ,'sectorCodeCompany' ,'sectorCompany' ,'segmentCompany'])
            # Display the DataFrame using Streamlit
            st.dataframe(df, use_container_width=True, hide_index = True)
        else:
            st.error("Tidak ada data yang tersedia.")

    elif database == 'Coin Value':
        cursor.execute("SELECT * FROM coinvalue")
        data = cursor.fetchall()
        if data:
            # Split and extract the elements from the tuple strings
            formatted_data = [(row[0], row[1], row[2]) for row in data]

            # Create a DataFrame from the formatted data
            df = pd.DataFrame(formatted_data, columns=['keyTime','keyCoin' ,'ValueCoin'])
            # Display the DataFrame using Streamlit
            st.dataframe(df, use_container_width=True, hide_index = True)
        else:
            st.error("Tidak ada data yang tersedia.")

    elif database == 'Stock Company':
        cursor.execute("SELECT * FROM stockcompany")
        data = cursor.fetchall()
        if data:
            # Split and extract the elements from the tuple strings
            formatted_data = [(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in data]

            # Create a DataFrame from the formatted data
            df = pd.DataFrame(formatted_data, columns=['keyTime','keyCompany' ,'openValueStock' ,'closeValueStock' ,'highValueStock' ,'lowValueStock' ,'quantityStock'])
            # Display the DataFrame using Streamlit
            st.dataframe(df, use_container_width=True, hide_index = True)
        else:
            st.error("Tidak ada data yang tersedia.")





elif selected_tab == "Stagging":
    database = st.selectbox("Pilih tabel source yang ingin ditampilkan:", ("Stagging Coin", "Stagging Time", "Stagging Company", "Stagging Coin Value" , "Stagging Stock Company"))

    if database == 'Stagging Coin':
        cursor1.execute("SELECT * FROM Stagging_Coin")
        data = cursor1.fetchall()
        if data:
            # Split and extract the elements from the tuple strings
            formatted_data = [(row[0], row[1]) for row in data]

            # Create a DataFrame from the formatted data
            df = pd.DataFrame(formatted_data, columns=['keyCoin','abbrevCoin'])

            # Display the DataFrame using Streamlit
            st.dataframe(df, use_container_width=True, hide_index = True)
            if st.button('Run Staging'):
                st.success("Stagging Coin berhasil dijalankan.")
                cursor1.execute("INSERT INTO Stagging.dbo.Stagging_Coin (keyCoin, abbrevCoin) SELECT s.keyCoin, s.abbrevCoin FROM Source.dbo.Coin s WHERE NOT EXISTS ( SELECT 1 FROM Stagging.dbo.Stagging_Coin t WHERE t.keyCoin = s.keyCoin )")

                cursor1.execute("CREATE TABLE temp_coin (keyCoin INT, abbrevCoin VARCHAR(50))")
                cursor1.execute("INSERT INTO temp_coin (keyCoin, abbrevCoin) SELECT keyCoin, abbrevCoin FROM Stagging.dbo.Stagging_Coin")
                connection1.commit()
        else:
            st.error("Tidak ada data yang tersedia.")
            if st.button('Run Staging'):
                st.success("Stagging Coin berhasil dijalankan.")
                cursor1.execute("INSERT INTO Stagging.dbo.Stagging_Coin (keyCoin, abbrevCoin) SELECT s.keyCoin, s.abbrevCoin FROM Source.dbo.Coin s WHERE NOT EXISTS ( SELECT 1 FROM Stagging.dbo.Stagging_Coin t WHERE t.keyCoin = s.keyCoin )")

                cursor1.execute("CREATE TABLE temp_coin (keyCoin INT, abbrevCoin VARCHAR(50))")
                cursor1.execute("INSERT INTO temp_coin (keyCoin, abbrevCoin) SELECT keyCoin, abbrevCoin FROM Stagging.dbo.Stagging_Coin")
                connection1.commit()

    elif database == 'Stagging Time':
        cursor1.execute("SELECT * FROM Stagging_Time")
        data = cursor1.fetchall()
        if data:
            # Split and extract the elements from the tuple strings
            formatted_data = [(row[0], row[1], row[2], row[3]) for row in data]

            # Create a DataFrame from the formatted data
            df = pd.DataFrame(formatted_data, columns=['keyTime' ,'datetime' ,'quarterTime' ,'semesterTime'])

            # Display the DataFrame using Streamlit
            st.dataframe(df, use_container_width=True, hide_index = True)
            if st.button('Run Staging'):
                st.success("Stagging Coin berhasil dijalankan.")
                cursor1.execute("INSERT INTO Stagging.dbo.Stagging_Time (keyTime, datetime, quarterTime, semesterTime) SELECT s.keyTime, s.datetime, s.quarterTime, s.semesterTime FROM Source.dbo.Time s WHERE NOT EXISTS (SELECT 1 FROM Stagging.dbo.Stagging_Time t WHERE t.keyTime = s.keyTime)")

                # Membuat tabel temp_Time tanpa kolom terpisah
                cursor1.execute("CREATE TABLE temp_Time (keyTime INT, datetime DATETIME, quarterTime INT, semesterTime INT)")

                # Menambahkan kolom-kolom terpisah setelah tabel dibuat
                cursor1.execute("ALTER TABLE temp_Time ADD YearColumn INT, MonthColumn INT, DayColumn INT")

                # Memasukkan data ke dalam tabel dengan memecah kolom datetime
                cursor1.execute("INSERT INTO temp_Time (keyTime, datetime, quarterTime, semesterTime) SELECT keyTime, datetime, quarterTime, semesterTime FROM Stagging.dbo.Stagging_Time")

                # Memperbarui nilai kolom terpisah sesuai dengan datetime
                cursor1.execute("UPDATE temp_Time SET YearColumn = DATEPART(YEAR, datetime), MonthColumn = DATEPART(MONTH, datetime), DayColumn = DATEPART(DAY, datetime)")

                cursor1.execute("ALTER TABLE temp_Time DROP COLUMN datetime")

                # Commit perubahan
                connection1.commit()

        else:
            st.error("Tidak ada data yang tersedia.")
            if st.button('Run Staging'):
                st.success("Stagging Coin berhasil dijalankan.")
                cursor1.execute("INSERT INTO Stagging.dbo.Stagging_Time (keyTime, datetime, quarterTime, semesterTime) SELECT s.keyTime, s.datetime, s.quarterTime, s.semesterTime FROM Source.dbo.Time s WHERE NOT EXISTS (SELECT 1 FROM Stagging.dbo.Stagging_Time t WHERE t.keyTime = s.keyTime)")

                # Membuat tabel temp_Time tanpa kolom terpisah
                cursor1.execute("CREATE TABLE temp_Time (keyTime INT, datetime DATETIME, quarterTime INT, semesterTime INT)")

                # Menambahkan kolom-kolom terpisah setelah tabel dibuat
                cursor1.execute("ALTER TABLE temp_Time ADD YearColumn INT, MonthColumn INT, DayColumn INT")

                # Memasukkan data ke dalam tabel dengan memecah kolom datetime
                cursor1.execute("INSERT INTO temp_Time (keyTime, datetime, quarterTime, semesterTime) SELECT keyTime, datetime, quarterTime, semesterTime FROM Stagging.dbo.Stagging_Time")

                # Memperbarui nilai kolom terpisah sesuai dengan datetime
                cursor1.execute("UPDATE temp_Time SET YearColumn = DATEPART(YEAR, datetime), MonthColumn = DATEPART(MONTH, datetime), DayColumn = DATEPART(DAY, datetime)")

                cursor1.execute("ALTER TABLE temp_Time DROP COLUMN datetime")

                # Commit perubahan
                connection1.commit()

    elif database == 'Stagging Stock Company':
        cursor1.execute("SELECT * FROM Stagging.dbo.stagging_stockcompany")
        data = cursor1.fetchall()
        if data:
            # Split and extract the elements from the tuple strings
            formatted_data = [(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in data]

            # Create a DataFrame from the formatted data
            df = pd.DataFrame(formatted_data, columns=['keyTime','keyCompany' ,'openValueStock' ,'closeValueStock' ,'highValueStock' ,'lowValueStock' ,'quantityStock'])

            # Display the DataFrame using Streamlit
            st.dataframe(df, use_container_width=True, hide_index=True)
            if st.button('Run Staging'):
                st.success("Stagging berhasil dijalankan.")

                # Insert into stagging_stockcompany
                cursor1.execute("INSERT INTO Stagging.dbo.stagging_stockcompany (keyTime, keyCompany, openValueStock, closeValueStock, highValueStock, lowValueStock, quantityStock) SELECT keyTime, keyCompany, openValueStock, closeValueStock, highValueStock, lowValueStock, quantityStock FROM Source.dbo.stockcompany s WHERE NOT EXISTS (SELECT 1 FROM Stagging.dbo.stagging_stockcompany t WHERE t.keyTime = s.keyTime AND t.keyCompany = s.keyCompany)")

                # Create temp_staggingstockcompany
                cursor1.execute("CREATE TABLE temp_staggingstockcompany (keyTime INT, keyCompany INT, openValueStock FLOAT, closeValueStock FLOAT, highValueStock FLOAT, lowValueStock FLOAT, quantityStock FLOAT)")

                # Insert into temp_staggingstockcompany
                cursor1.execute("INSERT INTO temp_staggingstockcompany (keyTime, keyCompany, openValueStock, closeValueStock, highValueStock, lowValueStock, quantityStock) SELECT keyTime, keyCompany, openValueStock, closeValueStock, highValueStock, lowValueStock, quantityStock FROM Stagging.dbo.stagging_stockcompany")

                # Commit perubahan
                connection1.commit()


        else:
            st.error("Tidak ada data yang tersedia.")
            if st.button('Run Staging'):
                st.success("Stagging berhasil dijalankan.")

                # Insert into stagging_stockcompany
                cursor1.execute("INSERT INTO Stagging.dbo.stagging_stockcompany (keyTime, keyCompany, openValueStock, closeValueStock, highValueStock, lowValueStock, quantityStock) SELECT keyTime, keyCompany, openValueStock, closeValueStock, highValueStock, lowValueStock, quantityStock FROM Source.dbo.stockcompany s WHERE NOT EXISTS (SELECT 1 FROM Stagging.dbo.stagging_stockcompany t WHERE t.keyTime = s.keyTime AND t.keyCompany = s.keyCompany)")

                # Create temp_staggingstockcompany
                cursor1.execute("CREATE TABLE temp_staggingstockcompany (keyTime INT, keyCompany INT, openValueStock FLOAT, closeValueStock FLOAT, highValueStock FLOAT, lowValueStock FLOAT, quantityStock FLOAT)")

                # Insert into temp_staggingstockcompany
                cursor1.execute("INSERT INTO temp_staggingstockcompany (keyTime, keyCompany, openValueStock, closeValueStock, highValueStock, lowValueStock, quantityStock) SELECT keyTime, keyCompany, openValueStock, closeValueStock, highValueStock, lowValueStock, quantityStock FROM Stagging.dbo.stagging_stockcompany")

                # Commit perubahan
                connection1.commit()


    elif database == 'Stagging Coin Value':
        cursor1.execute("SELECT * FROM Stagging.dbo.Stagging_CoinValue")
        data = cursor1.fetchall()

        if data:
            # Split and extract the elements from the tuple strings
            formatted_data = [(row[0], row[1], row[2]) for row in data]

            # Create a DataFrame from the formatted data
            df = pd.DataFrame(formatted_data, columns=['keyTime', 'keyCoin', 'ValueCoin'])

            # Display the DataFrame using Streamlit
            st.dataframe(df, use_container_width=True, hide_index=True)

            if st.button('Run Staging'):
                st.success("Stagging berhasil dijalankan.")

                # Insert into Stagging_CoinValue
                cursor1.execute("INSERT INTO Stagging.dbo.Stagging_CoinValue (keyTime, keyCoin, ValueCoin) SELECT keyTime, keyCoin, ValueCoin FROM Source.dbo.CoinValue s WHERE NOT EXISTS (SELECT 1 FROM Stagging.dbo.Stagging_CoinValue t WHERE t.keyTime = s.keyTime AND t.keyCoin = s.keyCoin)")

                # Create temp_staggingcoinvalue
                cursor1.execute("CREATE TABLE temp_staggingcoinvalue (keyTime INT, keyCoin INT, ValueCoin FLOAT)")

                # Insert into temp_staggingcoinvalue
                cursor1.execute("INSERT INTO temp_staggingcoinvalue (keyTime, keyCoin, ValueCoin) SELECT keyTime, keyCoin, ValueCoin FROM Stagging.dbo.Stagging_CoinValue")

                # Commit perubahan
                connection1.commit()

        else:
            st.error("Tidak ada data yang tersedia.")
            if st.button('Run Staging'):
                st.success("Stagging berhasil dijalankan.")

                # Insert into Stagging_CoinValue
                cursor1.execute("INSERT INTO Stagging.dbo.Stagging_CoinValue (keyTime, keyCoin, ValueCoin) SELECT keyTime, keyCoin, ValueCoin FROM Source.dbo.CoinValue s WHERE NOT EXISTS (SELECT 1 FROM Stagging.dbo.Stagging_CoinValue t WHERE t.keyTime = s.keyTime AND t.keyCoin = s.keyCoin)")

                # Create temp_staggingcoinvalue
                cursor1.execute("CREATE TABLE temp_staggingcoinvalue (keyTime INT, keyCoin INT, ValueCoin FLOAT)")

                # Insert into temp_staggingcoinvalue
                cursor1.execute("INSERT INTO temp_staggingcoinvalue (keyTime, keyCoin, ValueCoin) SELECT keyTime, keyCoin, ValueCoin FROM Stagging.dbo.Stagging_CoinValue")

                # Commit perubahan
                connection1.commit()




    elif database == 'Stagging Company':
        cursor1.execute("SELECT * FROM Stagging_Company")
        data = cursor1.fetchall()
        if data:
            # Split and extract the elements from the tuple strings
            formatted_data = [(row[0], row[1], row[2], row[3]) for row in data]

            # Create a DataFrame from the formatted data
            df = pd.DataFrame(formatted_data, columns=['keyCompany' ,'stockCodeCompany' ,'nameCompany' ,'sectorCompany'])

            # Display the DataFrame using Streamlit
            st.dataframe(df, use_container_width=True, hide_index = True)
            if st.button('Run Staging'):
                st.success("Stagging Coin berhasil dijalankan.")
                cursor1.execute("INSERT INTO Stagging.dbo.Stagging_Company (keyCompany, stockCodeCompany, nameCompany, sectorCompany) SELECT s.keyCompany, s.stockCodeCompany, s.nameCompany, s.sectorCompany FROM Source.dbo.Company s WHERE NOT EXISTS (SELECT 1 FROM Stagging.dbo.Stagging_Company t WHERE t.keyCompany = s.keyCompany)")

                cursor1.execute("CREATE TABLE temp_Company (keyCompany INT, stockCodeCompany VARCHAR(50), nameCompany VARCHAR(50), sectorCompany VARCHAR(100), sectorCodeCompany VARCHAR(50))")

                cursor1.execute("INSERT INTO temp_Company (keyCompany, stockCodeCompany, nameCompany, sectorCompany) SELECT keyCompany, stockCodeCompany, nameCompany, sectorCompany FROM Stagging.dbo.Stagging_Company")

                cursor1.execute("UPDATE temp_Company SET sectorCodeCompany = SUBSTRING(sectorCompany, CHARINDEX('(', sectorCompany) + 1, CHARINDEX(')', sectorCompany) - CHARINDEX('(', sectorCompany) - 1)")

                connection1.commit()

        else:
            st.error("Tidak ada data yang tersedia.")
            if st.button('Run Staging'):
                st.success("Stagging Coin berhasil dijalankan.")
                cursor1.execute("INSERT INTO Stagging.dbo.Stagging_Company (keyCompany, stockCodeCompany, nameCompany, sectorCompany) SELECT s.keyCompany, s.stockCodeCompany, s.nameCompany, s.sectorCompany FROM Source.dbo.Company s WHERE NOT EXISTS (SELECT 1 FROM Stagging.dbo.Stagging_Company t WHERE t.keyCompany = s.keyCompany)")

                cursor1.execute("CREATE TABLE temp_Company (keyCompany INT, stockCodeCompany VARCHAR(50), nameCompany VARCHAR(50), sectorCompany VARCHAR(100), sectorCodeCompany VARCHAR(50))")

                cursor1.execute("INSERT INTO temp_Company (keyCompany, stockCodeCompany, nameCompany, sectorCompany) SELECT keyCompany, stockCodeCompany, nameCompany, sectorCompany FROM Stagging.dbo.Stagging_Company")

                cursor1.execute("UPDATE temp_Company SET sectorCodeCompany = SUBSTRING(sectorCompany, CHARINDEX('(', sectorCompany) + 1, CHARINDEX(')', sectorCompany) - CHARINDEX('(', sectorCompany) - 1)")

                connection1.commit()



elif selected_tab == "Warehouse":
    database = st.selectbox("Pilih tabel source yang ingin ditampilkan:", ("Dim Coin", "Dim Time", "Dim Company", "Dim Coins Value", "Dim Stocks Company", "Fact Yearly Coin", "Fact Company Quantity"))

    cursor1.execute("Select tscv.keytime, tc.abbrevcoin, tscv.valuecoin, tt.yearcolumn from temp_coin as tc join temp_staggingcoinvalue tscv on tscv.keycoin = tc.keycoin join temp_time tt on tt.keytime = tscv.keytime")
    data_fakta = cursor1.fetchall()

    formatted_data = [(row[0], row[1],row[2], row[3]) for row in data_fakta]

    # Create a DataFrame from the formatted data
    df_yc = pd.DataFrame(formatted_data, columns=['keyTime', 'abbrevcoin', 'valuecoin', 'yearcolumn'])

    cursor1.execute("select tt.keytime, tssc.keycompany,quantitystock, namecompany, stockcodecompany, yearcolumn from temp_staggingstockcompany as tssc join temp_company as tc on tssc.keycompany = tc.keycompany join temp_time as tt on tt.keytime = tssc.keytime")
    data_fakta2 = cursor1.fetchall()

    formatted_data = [(row[0], row[1],row[2], row[3], row[4], row[5]) for row in data_fakta2]

    # Create a DataFrame from the formatted data
    df_cq = pd.DataFrame(formatted_data, columns=['keyTime', 'keycompany', 'quantity', 'namecompany', 'stockcodecompany', 'yearcolumn'])

    if database == 'Dim Coin':
        cursor2.execute("SELECT * FROM Dim_Coin")
        data = cursor2.fetchall()
        if data:
            # Split and extract the elements from the tuple strings
            formatted_data = [(row[0], row[1]) for row in data]

            # Create a DataFrame from the formatted data
            df = pd.DataFrame(formatted_data, columns=['keyCoin','abbrevCoin'])

            # Display the DataFrame using Streamlit
            st.dataframe(df, use_container_width=True, hide_index = True)
            if st.button('Run Warehouse'):
                st.success("Dim Coin berhasil dijalankan.")
                cursor2.execute("INSERT INTO Warehouse.dbo.Dim_Coin (keyCoin, abbrevCoin) SELECT s.keyCoin, s.abbrevCoin FROM Stagging.dbo.temp_Coin s WHERE NOT EXISTS ( SELECT 1 FROM Warehouse.dbo.Dim_Coin t WHERE t.keyCoin = s.keyCoin )")
                connection2.commit()
                # cursor1.execute("DROP TABLE Stagging.dbo.temp_coin")
                connection1.commit()
        else:
            st.error("Tidak ada data yang tersedia.")
            if st.button('Run Warehouse'):
                st.success("Warehouse Coin berhasil dijalankan.")
                cursor2.execute("INSERT INTO Warehouse.dbo.Dim_Coin (keyCoin, abbrevCoin) SELECT s.keyCoin, s.abbrevCoin FROM Stagging.dbo.temp_Coin s WHERE NOT EXISTS ( SELECT 1 FROM Warehouse.dbo.Dim_Coin t WHERE t.keyCoin = s.keyCoin )")
                connection2.commit()
                # cursor1.execute("DROP TABLE Stagging.dbo.temp_coin")
                connection1.commit()

    elif database == 'Dim Time':
        cursor2.execute("SELECT * FROM Dim_Time")
        data = cursor2.fetchall()
        if data:
            # Split and extract the elements from the tuple strings
            formatted_data = [(row[0], row[1], row[2], row[3], row[4], row[5]) for row in data]

            # Create a DataFrame from the formatted data
            df = pd.DataFrame(formatted_data, columns=['keyTime','YearColumn', 'MonthColumn', 'DayColumn,','quarterTime' ,'semesterTime'])

            # Display the DataFrame using Streamlit
            st.dataframe(df, use_container_width=True, hide_index = True)
            if st.button('Run Warehouse'):
                st.success("Dim Time berhasil dijalankan.")
                cursor2.execute("INSERT INTO warehouse.dbo.Dim_Time (keyTime, YearColumn, MonthColumn, DayColumn, quarterTime, semesterTime) SELECT s.keyTime, s.YearColumn, s.MonthColumn, s.DayColumn, s.quarterTime, s.semesterTime FROM Stagging.dbo.temp_Time s WHERE NOT EXISTS (SELECT 1 FROM warehouse.dbo.Dim_Time t WHERE t.keyTime = s.keyTime)")
                # Commit perubahan
                connection2.commit()
                # cursor1.execute('DROP TABLE Stagging.dbo.temp_Time')
                connection1.commit()

        else:
            st.error("Tidak ada data yang tersedia.")
            if st.button('Run Warehouse'):
                st.success("Dim Time berhasil dijalankan.")
                cursor2.execute("INSERT INTO warehouse.dbo.Dim_Time (keyTime, YearColumn,MonthColumn, DayColumn, quarterTime, semesterTime) SELECT s.keyTime, s.YearColumn, s.MonthColumn, s.DayColumn, s.quarterTime, s.semesterTime FROM Stagging.dbo.temp_Time s WHERE NOT EXISTS (SELECT 1 FROM warehouse.dbo.Dim_Time t WHERE t.keyTime = s.keyTime)")

                # Commit perubahan
                connection2.commit()
                # cursor1.execute('DROP TABLE Stagging.dbo.temp_Time')
                connection1.commit()

    elif database == 'Dim Stocks Company':
        cursor2.execute("SELECT * FROM warehouse.dbo.dim_stockcompany")
        data = cursor2.fetchall()

        if data:
            # Split and extract the elements from the tuple strings
            formatted_data = [(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in data]

            # Create a DataFrame from the formatted data
            df = pd.DataFrame(formatted_data, columns=['keyTime','keyCompany' ,'openValueStock' ,'closeValueStock' ,'highValueStock' ,'lowValueStock' ,'quantityStock'])

            # Display the DataFrame using Streamlit
            st.dataframe(df, use_container_width=True, hide_index=True)
            if st.button('Run Warehouse'):
                st.success("Dim Stock Company berhasil dijalankan.")

                # Insert into dim_stockcompany
                cursor2.execute("INSERT INTO warehouse.dbo.dim_stockcompany (keyTime, keyCompany, openValueStock, closeValueStock, highValueStock, lowValueStock, quantityStock) \
                    SELECT keyTime, keyCompany, openValueStock, closeValueStock, highValueStock, lowValueStock, quantityStock \
                    FROM Stagging.dbo.temp_staggingstockcompany s \
                    WHERE NOT EXISTS (SELECT 1 FROM warehouse.dbo.dim_stockcompany t WHERE t.keyTime = s.keyTime AND t.keyCompany = s.keyCompany)")

                # Commit perubahan
                connection2.commit()

                # Drop temp table in Stagging database
                # cursor1.execute('DROP TABLE Stagging.dbo.temp_staggingstockcompany')
                connection1.commit()

        else:
            st.error("Tidak ada data yang tersedia.")
            if st.button('Run Warehouse'):
                st.success("Dim Stock Company berhasil dijalankan.")

                # Insert into dim_stockcompany
                cursor2.execute("INSERT INTO warehouse.dbo.dim_stockcompany (keyTime, keyCompany, openValueStock, closeValueStock, highValueStock, lowValueStock, quantityStock) \
                    SELECT keyTime, keyCompany, openValueStock, closeValueStock, highValueStock, lowValueStock, quantityStock \
                    FROM Stagging.dbo.temp_staggingstockcompany s \
                    WHERE NOT EXISTS (SELECT 1 FROM warehouse.dbo.dim_stockcompany t WHERE t.keyTime = s.keyTime AND t.keyCompany = s.keyCompany)")

                # Commit perubahan
                connection2.commit()

                # Drop temp table in Stagging database
                # cursor1.execute('DROP TABLE Stagging.dbo.temp_staggingstockcompany')
                connection1.commit()


    elif database == 'Dim Company':
        cursor2.execute("SELECT * FROM warehouse.dbo.dim_company")
        data = cursor2.fetchall()

        if data:
            # Split and extract the elements from the tuple strings
            formatted_data = [(row[0], row[1], row[2], row[3], row[4]) for row in data]

            # Create a DataFrame from the formatted data
            df = pd.DataFrame(formatted_data, columns=['keyCompany', 'stockCodeCompany', 'nameCompany', 'sectorCompany', 'sectorCodeCompany'])

            # Display the DataFrame using Streamlit
            st.dataframe(df, use_container_width=True, hide_index=True)
            if st.button('Run Warehouse'):
                st.success("Dim Stock Company berhasil dijalankan.")

                # Insert into dim_stockcompany
                cursor2.execute("INSERT INTO Dim_Company (keyCompany, stockCodeCompany, nameCompany, sectorCompany, sectorCodeCompany) \
                    SELECT keyCompany, stockCodeCompany, nameCompany, sectorCompany, sectorCodeCompany \
                    FROM Stagging.dbo.temp_Company s \
                    WHERE NOT EXISTS (SELECT 1 FROM Dim_Company t WHERE t.keyCompany = s.keyCompany)")
                # Commit perubahan
                connection2.commit()

                # Drop temp table in Stagging database
                # cursor1.execute('DROP TABLE Stagging.dbo.temp_Company')
                connection1.commit()

        else:
            st.error("Tidak ada data yang tersedia.")
            if st.button('Run Warehouse'):
                st.success("Dim Stock Company berhasil dijalankan.")

                # Insert into dim_stockcompany
                cursor2.execute("INSERT INTO Dim_Company (keyCompany, stockCodeCompany, nameCompany, sectorCompany, sectorCodeCompany) \
                    SELECT keyCompany, stockCodeCompany, nameCompany, sectorCompany, sectorCodeCompany \
                    FROM Stagging.dbo.temp_Company s \
                    WHERE NOT EXISTS (SELECT 1 FROM Dim_Company t WHERE t.keyCompany = s.keyCompany)")
                # Commit perubahan
                connection2.commit()

                # Drop temp table in Stagging database
                # cursor1.execute('DROP TABLE Stagging.dbo.temp_Company')
                connection1.commit()


    elif database == 'Dim Coins Value':
        cursor2.execute("SELECT * FROM warehouse.dbo.dim_coinvalue")
        data = cursor2.fetchall()

        if data:
            # Split and extract the elements from the tuple strings
            formatted_data = [(row[0], row[1], row[2]) for row in data]

            # Create a DataFrame from the formatted data
            df = pd.DataFrame(formatted_data, columns=['keyTime', 'keyCoin', 'ValueCoin'])

            # Display the DataFrame using Streamlit
            st.dataframe(df, use_container_width=True, hide_index=True)
            if st.button('Run Warehouse'):
                st.success("Dim Coin Value berhasil dijalankan.")

                # Insert into dim_stockcompany
                cursor2.execute("INSERT INTO Dim_coinvalue (keyTime, keyCoin, ValueCoin) \
                    SELECT keyTime, keyCoin, ValueCoin \
                    FROM Stagging.dbo.temp_staggingcoinvalue s \
                    WHERE NOT EXISTS (SELECT 1 FROM Dim_coinvalue t WHERE t.keyTime = s.keyTime AND t.keyCoin = s.keyCoin)")

                # Commit perubahan
                connection2.commit()

                # Drop temp table in Stagging database
                # cursor1.execute('DROP TABLE Stagging.dbo.temp_staggingcoinvalue')
                connection1.commit()

        else:
            st.error("Tidak ada data yang tersedia.")
            if st.button('Run Warehouse'):
                st.success("Dim Coin Value berhasil dijalankan.")

                # Insert into dim_stockcompany
                cursor2.execute("INSERT INTO Dim_coinvalue (keyTime, keyCoin, ValueCoin) \
                    SELECT keyTime, keyCoin, ValueCoin \
                    FROM Stagging.dbo.temp_staggingcoinvalue s \
                    WHERE NOT EXISTS (SELECT 1 FROM Dim_coinvalue t WHERE t.keyTime = s.keyTime AND t.keyCoin = s.keyCoin)")

                # Commit perubahan
                connection2.commit()

                # Drop temp table in Stagging database
                # cursor1.execute('DROP TABLE Stagging.dbo.temp_staggingcoinvalue')
                connection1.commit()


    elif database == 'Fact Yearly Coin':
        options = list(df_yc['yearcolumn'].unique())
        a, b = st.select_slider("year:", options=options, value=(options[0], options[0]))
        abbrevcoin = st.multiselect("abbrevcoin:", df_yc['abbrevcoin'].unique())

        filtered_df = df_yc[(df_yc['yearcolumn'] >= a) & (df_yc['yearcolumn'] <= b) & (df_yc['abbrevcoin'].isin(abbrevcoin))]

        st.dataframe(filtered_df, use_container_width=True, hide_index=True)

        fig = px.line(filtered_df, x='keyTime', y='valuecoin', color='abbrevcoin')

        # Display the plot in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    elif database == 'Fact Company Quantity':
        options = list(sorted(df_cq['yearcolumn'].unique()))
        C, D = st.select_slider("year:", options=options, value=(options[12], options[15]))
        namecompany = st.multiselect("namecompany:", df_cq['namecompany'].unique(), default=df_cq['namecompany'].unique()[0])

        # Filtering DataFrame based on the selected range of years
        filtered_df = df_cq[(df_cq['yearcolumn'] >= C) & (df_cq['yearcolumn'] <= D)]

        # Further filtering based on selected namecompany
        filtered_df = filtered_df[filtered_df['namecompany'].isin(namecompany)]

        st.dataframe(filtered_df, use_container_width=True, hide_index=True)

        fig = px.line(filtered_df, x='keyTime', y='quantity', color='stockcodecompany')

        # Display the plot in Streamlit
        st.plotly_chart(fig, use_container_width=True)

