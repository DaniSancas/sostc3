#!/usr/bin/env python

import os
import csv
from sys import argv


lang_groups = {
    "general": {
        "javascript": "JavaScript",
        "java": "Java",
        "php": "PHP",
        "c": "C",
        "cpp": "C++",
        "python": "Python",
        "ruby": "Ruby",
        "go": "Go",
        "r": "R",
        "julia": "Julia",
        "objective-c": "Objective-C",
        "swift": "Swift",
        "rust": "Rust",
        "assembly": "Assembly",
        "perl": "Perl",
    },
    "mobile": {
        "android": "Android",
        "ios": "iOS",
        "windows-phone": "Windows Phone",
        "html5": "HTML5",
        "cordova": "Cordova/Phonegap",
    },
    "dot_net": {
        "c-sharp": "C#",
        "vb-net": "VB.NET",
        "asp-net": "ASP.NET",
        "f-sharp": "F#",
        # "ironpython": "IronPython",
    },
    "jvm": {
        "scala": "Scala",
        "clojure": "Clojure",
        "groovy": "Groovy",
        "jython": "Jython",
        "jruby": "Jruby",
    },
    "php_frameworks": {
        "symfony": "Symfony",
        "laravel": "Laravel",
        "codeigniter": "Codeigniter",
        "cakephp": "CakePHP",
        "yii": "Yii",
        "zend": "Zend",
    },
    "javascript_frontend": {
        "jquery": "jQuery",
        "mootools": "Mootools",
        "prototypejs": "Prototype",
        "reactjs": "ReactJS",
        "dojo": "Dojo",
    },
    "javascript_mvc": {
        "backbonejs": "BackboneJS",
        "emberjs": "EmberJS",
        "angularjs": "AngularJS",
        "angularjs2": "AngularJS2",
        "ionic": "Ionic",
    },
    "frontend_frameworks": {
        "bootstrap": "Bootstrap",
        "foundation": "Foundation",
    },
    "nodejs": {
        "nodejs": "NodeJS"
    },
    "sql_db": {
        "mysql": "MySQL",
        "sql-server": "SQL Server",
        "oracle": "Oracle",
        "postgresql": "PostgreSQL",
        "sqlite": "SQLite",
        "db2": "DB2",
    },
    "nosql_db": {
        "mongodb": "MongoDB",
        "cassandra": "Cassandra",
        "hbase": "HBase",
        "couchdb": "CouchDB",
        "redis": "Redis",
        "neo4j": "Neo4j",
    },
    "css": {
        "sass": "SASS",
        "less": "LESS",
    },
    "big_data": {
        "hadoop": "Hadoop",
        "hive": "Hive",
        "spark": "Spark",
        "impala": "Impala",
        "drill": "Drill",
        "pig": "Pig",
        "sqoop": "Sqoop",
        "flume": "Flume",
        "solr": "Solr",
    },
    "math": {
        "matlab": "Matlab",
        "octave": "Octave",
        "wolfram": "Mathematica",
    },
    "formats": {
        "xml": "XML",
        "yaml": "YAML",
        "json": "JSON",
    },
    "old": {
        "lisp": "Lisp",
        "prolog": "Prolog",
        "fortran": "Fortran",
        "cobol": "Cobol",
    },
    "death": {
        "vbscript": "VBscript",
        "vb6": "Visual Basic 6",
        "asp": "ASP",
        "delphi": "Delphi",
        "flash": "Flash",
    }
}


def merge_and_dump(inputdir, outputdir):
    """Groups relationed Language coefficient CSV files and generates chart-ready CSV files.
    Example of usage: $ coefficient_to_chart.py <input_dir> <output_dir>"""
    # Get absolute paths, to avoid problems
    abs_input_dir = os.path.abspath(inputdir)
    abs_output_dir = os.path.abspath(outputdir)
    for lang in lang_groups:
        # For every group of languages, get absolute path to CSV files (keys) and formatted header name (values)
        lang_keys = list(map(lambda x: os.path.join(abs_input_dir, "{}.csv".format(x)),
                             sorted(list(lang_groups[lang].keys()))))
        lang_values = sorted(list(lang_groups[lang].values()))

        with open(os.path.join(abs_output_dir, "{}.csv".format(lang)), 'w') as result_csv:
            # Create CSV file for chart
            result_writer = csv.writer(result_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            buffer_csv = []  # 2-dimmension array containing each coefficient of each timelapse of each language
            timelapse = []  # year-month-day array, filled once per group of languages
            fill_timelapse = True
            for key, lang_file in enumerate(lang_keys):
                # For each language in the group
                lang_coefficients = [lang_values[key]]  # Array with header (formatted language name) and coefficients
                with open(lang_file) as source_csv:
                    # Open file for reading and skip header row
                    source_reader = csv.reader(source_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    next(source_reader)

                    for line in source_reader:
                        # For each row, get coefficient and, if not already filled, get the year-month-day value
                        lang_coefficients.append(line[2])
                        if fill_timelapse:
                            timelapse.append("{}-01".format(line[1]))
                    fill_timelapse = False  # Once the first language completed, stop retrieving year-month-day values
                buffer_csv.append(lang_coefficients)  # Add the [header, coefficients...] array to buffer array

            # Once every language in the group is retrieved, write the buffer array to chart CSV file
            # Firstly, write the header
            buffer_row = ["x"]  # First header item is "X" axis
            for key, value in enumerate(buffer_csv):
                # For every language in the group, write it's name as a new column
                buffer_row.append(buffer_csv[key][0])
            result_writer.writerow(buffer_row)

            # Once the header is written, write a row for every timelapse, with year-month-day values and coefficients
            for key_lapse, value_lapse in enumerate(timelapse):
                buffer_row = [value_lapse]  # First item is year-month-day
                for key, value in enumerate(buffer_csv):
                    # For every language in the group, write the coefficient for the timelapse as a new column
                    buffer_row.append(buffer_csv[key][key_lapse+1])  # Index equal to timelapse's index + 1
                result_writer.writerow(buffer_row)


if __name__ == "__main__":
    if len(argv) != 3 or argv[1] == "--help" or argv[1] == "-h":
        print(merge_and_dump.__doc__)
    else:
        merge_and_dump(argv[1], argv[2])
