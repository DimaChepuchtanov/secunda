import pandas as pd


class ExcelGenerate:
    def __init__(self):
        pass

    def generate_excel(self, dataframe_dict: list):
        """
        Generate an Excel file with multiple sheets from a list of dataframes.

        Args:
            dataframe_dict (list): List of dictionaries containing sheet names and dataframes.
        """
        with pd.ExcelWriter('result.xlsx', engine='xlsxwriter') as writer:
            for i in dataframe_dict:
                for key, value in i.items():
                    value.to_excel(writer, sheet_name=key, index=False,)

                    workbook = writer.book
                    worksheet = writer.sheets[key]

                    for i, col in enumerate(value.columns):
                        column_length = max(
                            value[col].astype(str).map(len).max(),
                            len(col)
                        )
                        worksheet.set_column(i, i, column_length + 2)

    def update_dataframe(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Update the dataframe by dropping unnecessary columns and renaming for Excel output.

        Args:
            dataframe (pd.DataFrame): Input dataframe.

        Returns:
            dict: Dictionary with title as key and updated dataframe as value.
        """
        headers = dataframe.columns.values.tolist()

        if "Result" in headers:
            headers = [x for x in headers if x not in ['tradetime', 'Result', 'tradedate']]
            for header in headers:
                if "Курс " in header:
                    headers.remove(header)
            dataframe = dataframe.drop(headers, axis=1)
            title = "Result"
        else:
            headers = ['clearing', 'rate', 'tradetime', 'secid', 'tradedate']
            dataframe = dataframe.drop(headers, axis=1)
            title = dataframe.columns.values.tolist()[0].split()[1].replace("/", "_to_")

        return {title: dataframe}
