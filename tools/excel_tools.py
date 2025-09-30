import os
import time
import pandas as pd
import numpy as np
import zipfile
import json
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
import tempfile

class ExcelProcessor:
    def __init__(self):
        self.output_dir = 'output'
        os.makedirs(self.output_dir, exist_ok=True)
    
    def process(self, tool_name, data, task_id):
        """Main processing method that routes to specific tool handlers"""
        
        time.sleep(1)  # Initial setup time
        
        method_map = {
            'excel_csv_converter': self.excel_to_csv,
            'csv_excel_converter': self.csv_to_excel,
            'excel_deduplicator': self.deduplicate_excel,
            'excel_cleaner': self.clean_excel,
            'csv_validator': self.validate_csv,
            'bulk_csv_sql': self.csv_to_sql,
            'csv_json_converter': self.csv_json_converter,
            'excel_merger': self.merge_excel,
            'excel_pivot_generator': self.generate_pivot,
            'excel_chart_generator': self.generate_charts
        }
        
        handler = method_map.get(tool_name)
        if not handler:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        return handler(data, task_id)
    
    def update_progress(self, task_id, progress):
        """Update task progress"""
        from app import TaskManager
        TaskManager.update_progress(task_id, progress)
    
    def excel_to_csv(self, data, task_id):
        """Convert Excel files to CSV"""
        self.update_progress(task_id, 20)
        
        files = data.get('files', [])
        output_files = []
        
        for i, file_info in enumerate(files):
            input_path = file_info['filepath']
            base_name = os.path.basename(input_path).split('.')[0]
            
            try:
                # Read Excel file
                excel_file = pd.ExcelFile(input_path)
                
                if len(excel_file.sheet_names) == 1:
                    # Single sheet - create one CSV
                    df = pd.read_excel(input_path)
                    output_path = os.path.join(self.output_dir, f"{task_id}_{base_name}.csv")
                    df.to_csv(output_path, index=False)
                    output_files.append(output_path)
                else:
                    # Multiple sheets - create CSV for each
                    for sheet_name in excel_file.sheet_names:
                        df = pd.read_excel(input_path, sheet_name=sheet_name)
                        csv_filename = f"{task_id}_{base_name}_{sheet_name}.csv"
                        output_path = os.path.join(self.output_dir, csv_filename)
                        df.to_csv(output_path, index=False)
                        output_files.append(output_path)
                
            except Exception as e:
                # Create error report
                error_path = os.path.join(self.output_dir, f"{task_id}_{base_name}_error.txt")
                with open(error_path, 'w') as f:
                    f.write(f"Error converting {base_name}: {str(e)}")
                output_files.append(error_path)
            
            # Update progress
            progress = 20 + (70 * (i + 1) / len(files))
            self.update_progress(task_id, progress)
        
        # Create ZIP if multiple files
        if len(output_files) > 1:
            zip_path = os.path.join(self.output_dir, f"{task_id}_excel_to_csv.zip")
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file_path in output_files:
                    zipf.write(file_path, os.path.basename(file_path))
                    os.remove(file_path)
            final_output = zip_path
        else:
            final_output = output_files[0]
        
        self.update_progress(task_id, 100)
        return {'output_path': final_output, 'filename': os.path.basename(final_output)}
    
    def csv_to_excel(self, data, task_id):
        """Convert CSV files to Excel"""
        self.update_progress(task_id, 20)
        
        files = data.get('files', [])
        
        if len(files) == 1:
            # Single CSV to Excel
            file_info = files[0]
            input_path = file_info['filepath']
            base_name = os.path.basename(input_path).split('.')[0]
            output_path = os.path.join(self.output_dir, f"{task_id}_{base_name}.xlsx")
            
            try:
                df = pd.read_csv(input_path)
                df.to_excel(output_path, index=False)
            except Exception as e:
                # Create simple Excel with error message
                error_df = pd.DataFrame({'Error': [f"Failed to convert {base_name}: {str(e)}"]})
                error_df.to_excel(output_path, index=False)
            
            final_output = output_path
        else:
            # Multiple CSVs to single Excel with multiple sheets
            output_path = os.path.join(self.output_dir, f"{task_id}_combined_csvs.xlsx")
            
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                for i, file_info in enumerate(files):
                    input_path = file_info['filepath']
                    sheet_name = os.path.basename(input_path).split('.')[0][:31]  # Excel sheet name limit
                    
                    try:
                        df = pd.read_csv(input_path)
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                    except Exception as e:
                        error_df = pd.DataFrame({'Error': [f"Failed to process: {str(e)}"]})
                        error_df.to_excel(writer, sheet_name=f"Error_{i+1}", index=False)
                    
                    # Update progress
                    progress = 20 + (70 * (i + 1) / len(files))
                    self.update_progress(task_id, progress)
            
            final_output = output_path
        
        self.update_progress(task_id, 100)
        return {'output_path': final_output, 'filename': os.path.basename(final_output)}
    
    def deduplicate_excel(self, data, task_id):
        """Remove duplicate rows from Excel/CSV files"""
        self.update_progress(task_id, 20)
        
        files = data.get('files', [])
        output_files = []
        
        for i, file_info in enumerate(files):
            input_path = file_info['filepath']
            base_name = os.path.basename(input_path).split('.')[0]
            
            try:
                # Read file
                if input_path.endswith('.csv'):
                    df = pd.read_csv(input_path)
                    output_path = os.path.join(self.output_dir, f"{task_id}_{base_name}_dedup.csv")
                    save_func = lambda: df.to_csv(output_path, index=False)
                else:
                    df = pd.read_excel(input_path)
                    output_path = os.path.join(self.output_dir, f"{task_id}_{base_name}_dedup.xlsx")
                    save_func = lambda: df.to_excel(output_path, index=False)
                
                # Remove duplicates
                original_count = len(df)
                df_dedup = df.drop_duplicates()
                duplicate_count = original_count - len(df_dedup)
                
                # Add summary row
                summary_row = pd.DataFrame({
                    'SUMMARY': [f"Original rows: {original_count}, Duplicates removed: {duplicate_count}, Final rows: {len(df_dedup)}"],
                    **{col: [''] for col in df_dedup.columns[1:]}  # Fill other columns with empty strings
                })
                
                # Combine data
                df_final = pd.concat([summary_row, df_dedup], ignore_index=True)
                
                # Save
                if input_path.endswith('.csv'):
                    df_final.to_csv(output_path, index=False)
                else:
                    df_final.to_excel(output_path, index=False)
                
                output_files.append(output_path)
                
            except Exception as e:
                # Create error file
                error_path = os.path.join(self.output_dir, f"{task_id}_{base_name}_error.txt")
                with open(error_path, 'w') as f:
                    f.write(f"Error deduplicating {base_name}: {str(e)}")
                output_files.append(error_path)
            
            # Update progress
            progress = 20 + (70 * (i + 1) / len(files))
            self.update_progress(task_id, progress)
        
        # Create ZIP if multiple files
        if len(output_files) > 1:
            zip_path = os.path.join(self.output_dir, f"{task_id}_deduplicated.zip")
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file_path in output_files:
                    zipf.write(file_path, os.path.basename(file_path))
                    os.remove(file_path)
            final_output = zip_path
        else:
            final_output = output_files[0]
        
        self.update_progress(task_id, 100)
        return {'output_path': final_output, 'filename': os.path.basename(final_output)}
    
    def clean_excel(self, data, task_id):
        """Clean Excel/CSV files by removing empty cells and standardizing format"""
        self.update_progress(task_id, 20)
        
        files = data.get('files', [])
        output_files = []
        
        for i, file_info in enumerate(files):
            input_path = file_info['filepath']
            base_name = os.path.basename(input_path).split('.')[0]
            
            try:
                # Read file
                if input_path.endswith('.csv'):
                    df = pd.read_csv(input_path)
                    output_path = os.path.join(self.output_dir, f"{task_id}_{base_name}_cleaned.csv")
                else:
                    df = pd.read_excel(input_path)
                    output_path = os.path.join(self.output_dir, f"{task_id}_{base_name}_cleaned.xlsx")
                
                # Cleaning operations
                original_shape = df.shape
                
                # Remove completely empty rows and columns
                df = df.dropna(how='all')  # Remove rows where all values are NaN
                df = df.dropna(axis=1, how='all')  # Remove columns where all values are NaN
                
                # Strip whitespace from string columns
                for col in df.select_dtypes(include=['object']).columns:
                    df[col] = df[col].astype(str).str.strip()
                    df[col] = df[col].replace('nan', pd.NA)  # Convert 'nan' strings back to actual NaN
                
                # Standardize column names
                df.columns = df.columns.str.strip().str.replace(' ', '_').str.lower()
                
                cleaned_shape = df.shape
                
                # Create summary
                summary = {
                    'original_rows': original_shape[0],
                    'original_columns': original_shape[1],
                    'cleaned_rows': cleaned_shape[0],
                    'cleaned_columns': cleaned_shape[1],
                    'rows_removed': original_shape[0] - cleaned_shape[0],
                    'columns_removed': original_shape[1] - cleaned_shape[1]
                }
                
                # Add summary as first row
                summary_df = pd.DataFrame([summary])
                df_with_summary = pd.concat([summary_df, df], ignore_index=True)
                
                # Save
                if input_path.endswith('.csv'):
                    df_with_summary.to_csv(output_path, index=False)
                else:
                    df_with_summary.to_excel(output_path, index=False)
                
                output_files.append(output_path)
                
            except Exception as e:
                error_path = os.path.join(self.output_dir, f"{task_id}_{base_name}_error.txt")
                with open(error_path, 'w') as f:
                    f.write(f"Error cleaning {base_name}: {str(e)}")
                output_files.append(error_path)
            
            progress = 20 + (70 * (i + 1) / len(files))
            self.update_progress(task_id, progress)
        
        # Create ZIP if multiple files
        if len(output_files) > 1:
            zip_path = os.path.join(self.output_dir, f"{task_id}_cleaned_files.zip")
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file_path in output_files:
                    zipf.write(file_path, os.path.basename(file_path))
                    os.remove(file_path)
            final_output = zip_path
        else:
            final_output = output_files[0]
        
        self.update_progress(task_id, 100)
        return {'output_path': final_output, 'filename': os.path.basename(final_output)}
    
    def validate_csv(self, data, task_id):
        """Validate CSV files for errors and inconsistencies"""
        self.update_progress(task_id, 20)
        
        files = data.get('files', [])
        validation_results = []
        
        for i, file_info in enumerate(files):
            input_path = file_info['filepath']
            filename = os.path.basename(input_path)
            
            try:
                df = pd.read_csv(input_path)
                
                # Validation checks
                result = {
                    'filename': filename,
                    'total_rows': len(df),
                    'total_columns': len(df.columns),
                    'empty_rows': df.isnull().all(axis=1).sum(),
                    'empty_columns': df.isnull().all(axis=0).sum(),
                    'duplicate_rows': df.duplicated().sum(),
                    'missing_values': df.isnull().sum().sum(),
                    'data_types': df.dtypes.to_dict(),
                    'issues': []
                }
                
                # Check for issues
                if result['empty_rows'] > 0:
                    result['issues'].append(f"{result['empty_rows']} empty rows found")
                
                if result['empty_columns'] > 0:
                    result['issues'].append(f"{result['empty_columns']} empty columns found")
                
                if result['duplicate_rows'] > 0:
                    result['issues'].append(f"{result['duplicate_rows']} duplicate rows found")
                
                if result['missing_values'] > 0:
                    result['issues'].append(f"{result['missing_values']} missing values found")
                
                # Check for inconsistent data types in columns
                for col in df.columns:
                    if df[col].dtype == 'object':
                        # Check if column should be numeric
                        non_null_values = df[col].dropna()
                        if len(non_null_values) > 0:
                            try:
                                pd.to_numeric(non_null_values)
                                result['issues'].append(f"Column '{col}' contains numeric data but is stored as text")
                            except:
                                pass
                
                validation_results.append(result)
                
            except Exception as e:
                validation_results.append({
                    'filename': filename,
                    'error': str(e),
                    'issues': [f"Failed to read file: {str(e)}"]
                })
            
            progress = 20 + (70 * (i + 1) / len(files))
            self.update_progress(task_id, progress)
        
        # Create validation report
        output_path = os.path.join(self.output_dir, f"{task_id}_validation_report.xlsx")
        
        # Convert results to DataFrame
        report_data = []
        for result in validation_results:
            row = {
                'filename': result['filename'],
                'total_rows': result.get('total_rows', 'N/A'),
                'total_columns': result.get('total_columns', 'N/A'),
                'empty_rows': result.get('empty_rows', 'N/A'),
                'empty_columns': result.get('empty_columns', 'N/A'),
                'duplicate_rows': result.get('duplicate_rows', 'N/A'),
                'missing_values': result.get('missing_values', 'N/A'),
                'issues': '; '.join(result.get('issues', [])),
                'status': 'Valid' if len(result.get('issues', [])) == 0 else 'Issues Found'
            }
            report_data.append(row)
        
        report_df = pd.DataFrame(report_data)
        report_df.to_excel(output_path, index=False)
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def csv_to_sql(self, data, task_id):
        """Convert CSV files to SQL INSERT statements"""
        self.update_progress(task_id, 20)
        
        files = data.get('files', [])
        sql_statements = []
        
        for i, file_info in enumerate(files):
            input_path = file_info['filepath']
            table_name = os.path.basename(input_path).split('.')[0].lower().replace(' ', '_')
            
            try:
                df = pd.read_csv(input_path)
                
                # Clean column names for SQL
                df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('-', '_').str.lower()
                
                # Generate CREATE TABLE statement
                create_table = f"CREATE TABLE {table_name} (\n"
                column_defs = []
                
                for col in df.columns:
                    # Determine data type
                    if df[col].dtype in ['int64', 'int32']:
                        col_type = 'INTEGER'
                    elif df[col].dtype in ['float64', 'float32']:
                        col_type = 'DECIMAL(10,2)'
                    else:
                        col_type = 'VARCHAR(255)'
                    
                    column_defs.append(f"    {col} {col_type}")
                
                create_table += ",\n".join(column_defs) + "\n);\n\n"
                sql_statements.append(create_table)
                
                # Generate INSERT statements
                for _, row in df.iterrows():
                    values = []
                    for val in row:
                        if pd.isna(val):
                            values.append('NULL')
                        elif isinstance(val, str):
                            # Escape single quotes
                            escaped_val = str(val).replace("'", "''")
                            values.append(f"'{escaped_val}'")
                        else:
                            values.append(str(val))
                    
                    insert_stmt = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({', '.join(values)});\n"
                    sql_statements.append(insert_stmt)
                
                sql_statements.append("\n")  # Add spacing between tables
                
            except Exception as e:
                error_comment = f"-- Error processing {os.path.basename(input_path)}: {str(e)}\n\n"
                sql_statements.append(error_comment)
            
            progress = 20 + (70 * (i + 1) / len(files))
            self.update_progress(task_id, progress)
        
        # Write SQL file
        output_path = os.path.join(self.output_dir, f"{task_id}_database_import.sql")
        with open(output_path, 'w') as f:
            f.write("-- Generated SQL Import Script\n")
            f.write("-- Created from CSV files\n\n")
            f.writelines(sql_statements)
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def csv_json_converter(self, data, task_id):
        """Convert between CSV and JSON formats"""
        self.update_progress(task_id, 20)
        
        files = data.get('files', [])
        output_files = []
        
        for i, file_info in enumerate(files):
            input_path = file_info['filepath']
            base_name = os.path.basename(input_path).split('.')[0]
            
            try:
                if input_path.endswith('.csv'):
                    # CSV to JSON
                    df = pd.read_csv(input_path)
                    output_path = os.path.join(self.output_dir, f"{task_id}_{base_name}.json")
                    
                    # Convert to JSON with proper formatting
                    json_data = df.to_dict('records')
                    with open(output_path, 'w') as f:
                        json.dump(json_data, f, indent=2, default=str)
                
                elif input_path.endswith('.json'):
                    # JSON to CSV
                    with open(input_path, 'r') as f:
                        json_data = json.load(f)
                    
                    # Handle different JSON structures
                    if isinstance(json_data, list):
                        df = pd.DataFrame(json_data)
                    elif isinstance(json_data, dict):
                        df = pd.DataFrame([json_data])
                    else:
                        raise ValueError("Unsupported JSON structure")
                    
                    output_path = os.path.join(self.output_dir, f"{task_id}_{base_name}.csv")
                    df.to_csv(output_path, index=False)
                
                output_files.append(output_path)
                
            except Exception as e:
                error_path = os.path.join(self.output_dir, f"{task_id}_{base_name}_error.txt")
                with open(error_path, 'w') as f:
                    f.write(f"Error converting {base_name}: {str(e)}")
                output_files.append(error_path)
            
            progress = 20 + (70 * (i + 1) / len(files))
            self.update_progress(task_id, progress)
        
        # Create ZIP if multiple files
        if len(output_files) > 1:
            zip_path = os.path.join(self.output_dir, f"{task_id}_converted_files.zip")
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file_path in output_files:
                    zipf.write(file_path, os.path.basename(file_path))
                    os.remove(file_path)
            final_output = zip_path
        else:
            final_output = output_files[0]
        
        self.update_progress(task_id, 100)
        return {'output_path': final_output, 'filename': os.path.basename(final_output)}
    
    def merge_excel(self, data, task_id):
        """Merge multiple Excel/CSV files into one"""
        self.update_progress(task_id, 20)
        
        files = data.get('files', [])
        if len(files) < 2:
            raise ValueError("At least 2 files are required for merging")
        
        merged_data = []
        
        for i, file_info in enumerate(files):
            input_path = file_info['filepath']
            filename = os.path.basename(input_path)
            
            try:
                if input_path.endswith('.csv'):
                    df = pd.read_csv(input_path)
                else:
                    df = pd.read_excel(input_path)
                
                # Add source file column
                df['source_file'] = filename
                merged_data.append(df)
                
            except Exception as e:
                # Create error entry
                error_df = pd.DataFrame({
                    'error': [f"Failed to read {filename}: {str(e)}"],
                    'source_file': [filename]
                })
                merged_data.append(error_df)
            
            progress = 20 + (60 * (i + 1) / len(files))
            self.update_progress(task_id, progress)
        
        # Combine all data
        try:
            final_df = pd.concat(merged_data, ignore_index=True, sort=False)
        except Exception as e:
            # If concat fails, create a simple combination
            final_df = pd.DataFrame({'error': [f"Failed to merge files: {str(e)}"]})
        
        # Save merged file
        output_path = os.path.join(self.output_dir, f"{task_id}_merged_data.xlsx")
        final_df.to_excel(output_path, index=False)
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def generate_pivot(self, data, task_id):
        """Generate pivot table from data"""
        self.update_progress(task_id, 30)
        
        files = data.get('files', [])
        if not files:
            raise ValueError("No files provided")
        
        # Use first file for pivot generation
        input_path = files[0]['filepath']
        
        try:
            if input_path.endswith('.csv'):
                df = pd.read_csv(input_path)
            else:
                df = pd.read_excel(input_path)
            
            self.update_progress(task_id, 50)
            
            # Create basic pivot table
            # For demo purposes, we'll create a simple pivot if possible
            numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
            
            if len(numeric_columns) > 0 and len(categorical_columns) > 0:
                # Create pivot table
                pivot_table = pd.pivot_table(
                    df, 
                    values=numeric_columns[0], 
                    index=categorical_columns[0], 
                    aggfunc=['count', 'mean'] if len(numeric_columns) > 0 else 'count'
                )
                
                output_path = os.path.join(self.output_dir, f"{task_id}_pivot_table.xlsx")
                pivot_table.to_excel(output_path)
            else:
                # Create summary statistics instead
                summary = df.describe(include='all')
                output_path = os.path.join(self.output_dir, f"{task_id}_data_summary.xlsx")
                summary.to_excel(output_path)
            
        except Exception as e:
            # Create error report
            output_path = os.path.join(self.output_dir, f"{task_id}_pivot_error.txt")
            with open(output_path, 'w') as f:
                f.write(f"Error generating pivot table: {str(e)}")
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def generate_charts(self, data, task_id):
        """Generate charts from Excel/CSV data"""
        self.update_progress(task_id, 30)
        
        files = data.get('files', [])
        if not files:
            raise ValueError("No files provided")
        
        input_path = files[0]['filepath']
        
        try:
            if input_path.endswith('.csv'):
                df = pd.read_csv(input_path)
            else:
                df = pd.read_excel(input_path)
            
            self.update_progress(task_id, 50)
            
            # Generate basic charts
            plt.style.use('default')
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            fig.suptitle('Data Analysis Charts', fontsize=16)
            
            # Chart 1: Data info
            ax1 = axes[0, 0]
            ax1.text(0.1, 0.5, f"Dataset Info:\nRows: {len(df)}\nColumns: {len(df.columns)}\nMemory: {df.memory_usage().sum()} bytes", 
                    transform=ax1.transAxes, fontsize=12, verticalalignment='center')
            ax1.set_title('Dataset Overview')
            ax1.axis('off')
            
            # Chart 2: Missing values
            ax2 = axes[0, 1]
            missing_data = df.isnull().sum()
            if missing_data.sum() > 0:
                missing_data[missing_data > 0].plot(kind='bar', ax=ax2)
                ax2.set_title('Missing Values by Column')
                ax2.tick_params(axis='x', rotation=45)
            else:
                ax2.text(0.5, 0.5, 'No missing values', transform=ax2.transAxes, 
                        ha='center', va='center', fontsize=12)
                ax2.set_title('Missing Values')
                ax2.axis('off')
            
            # Chart 3: Numeric data distribution
            ax3 = axes[1, 0]
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                df[numeric_cols[0]].hist(ax=ax3, bins=20)
                ax3.set_title(f'Distribution of {numeric_cols[0]}')
            else:
                ax3.text(0.5, 0.5, 'No numeric columns', transform=ax3.transAxes, 
                        ha='center', va='center', fontsize=12)
                ax3.set_title('Numeric Distribution')
                ax3.axis('off')
            
            # Chart 4: Data types
            ax4 = axes[1, 1]
            dtype_counts = df.dtypes.value_counts()
            dtype_counts.plot(kind='pie', ax=ax4, autopct='%1.1f%%')
            ax4.set_title('Data Types Distribution')
            
            plt.tight_layout()
            
            # Save chart
            output_path = os.path.join(self.output_dir, f"{task_id}_data_charts.png")
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
        except Exception as e:
            # Create simple text chart
            output_path = os.path.join(self.output_dir, f"{task_id}_chart_error.txt")
            with open(output_path, 'w') as f:
                f.write(f"Error generating charts: {str(e)}")
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}