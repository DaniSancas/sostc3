#!/usr/bin/env python

import os
import csv
from sys import argv
import pandas as pd


lang_groups = {
    "general": {
        "javascript": "JavaScript",
        "java": "Java",
        "php": "PHP",
        "c": "C",
        "cpp": "C++",
        "c-sharp": "C#",
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
        "cobol": "COBOL",
    },
    "dead": {
        "vbscript": "VBscript",
        "vb6": "Visual Basic 6",
        "asp": "ASP",
        "delphi": "Delphi",
        "flash": "Flash",
    },
    "all": {
        "javascript": "JavaScript",
        "java": "Java",
        "php": "PHP",
        "c": "C",
        "cpp": "C++",
        "c-sharp": "C#",
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
        "android": "Android",
        "ios": "iOS",
        "windows-phone": "Windows Phone",
        "html5": "HTML5",
        "cordova": "Cordova/Phonegap",
        "vb-net": "VB.NET",
        "asp-net": "ASP.NET",
        "f-sharp": "F#",
        "scala": "Scala",
        "clojure": "Clojure",
        "groovy": "Groovy",
        "jython": "Jython",
        "jruby": "Jruby",
        "symfony": "Symfony",
        "laravel": "Laravel",
        "codeigniter": "Codeigniter",
        "cakephp": "CakePHP",
        "yii": "Yii",
        "zend": "Zend",
        "jquery": "jQuery",
        "mootools": "Mootools",
        "prototypejs": "Prototype",
        "reactjs": "ReactJS",
        "dojo": "Dojo",
        "backbonejs": "BackboneJS",
        "emberjs": "EmberJS",
        "angularjs": "AngularJS",
        "angularjs2": "AngularJS2",
        "ionic": "Ionic",
        "bootstrap": "Bootstrap",
        "foundation": "Foundation",
        "nodejs": "NodeJS",
        "mysql": "MySQL",
        "sql-server": "SQL Server",
        "oracle": "Oracle",
        "postgresql": "PostgreSQL",
        "sqlite": "SQLite",
        "db2": "DB2",
        "mongodb": "MongoDB",
        "cassandra": "Cassandra",
        "hbase": "HBase",
        "couchdb": "CouchDB",
        "redis": "Redis",
        "neo4j": "Neo4j",
        "sass": "SASS",
        "less": "LESS",
        "hadoop": "Hadoop",
        "hive": "Hive",
        "spark": "Spark",
        "impala": "Impala",
        "drill": "Drill",
        "pig": "Pig",
        "sqoop": "Sqoop",
        "flume": "Flume",
        "solr": "Solr",
        "matlab": "Matlab",
        "octave": "Octave",
        "wolfram": "Mathematica",
        "xml": "XML",
        "yaml": "YAML",
        "json": "JSON",
        "lisp": "Lisp",
        "prolog": "Prolog",
        "fortran": "Fortran",
        "cobol": "COBOL",
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
    for lang in lang_groups:
        # For every group of languages, get absolute path to CSV files (keys) and formatted header name (values)
        # Returns two lists (key and value) sorted the same way (Alphabetical
        sorted_keys, lang_values = zip(*[(key, value) for key, value in sorted(lang_groups[lang].items())])
        lang_keys = list(map(lambda x: os.path.join(os.path.abspath(inputdir), "{}.csv".format(x)), sorted_keys))

        csv_df = pd.DataFrame(columns=(('x',) + lang_values))
        fill_timelapse = True
        for key, lang_file in enumerate(lang_keys):
            # For each language in the group
            with open(lang_file) as source_csv:
                # Open file for reading and skip header row
                source_reader = csv.reader(source_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                next(source_reader)

                if fill_timelapse:
                    timelapse, lang_coefficients = zip(*[("{}-01".format(line[1]), line[2]) for line in source_reader])
                    csv_df['x'] = pd.DataFrame.from_dict({'x': timelapse})  # Add X axis (time-series)
                    fill_timelapse = False  # Once the first language completed, stop retrieving year-month-day values
                else:
                    lang_coefficients = [line[2] for line in source_reader]

            csv_df[lang_values[key]] = pd.DataFrame({lang_values[key]: lang_coefficients})  # Add each lang coefficient
        # Dump DataFrame to CSV
        csv_df.to_csv(os.path.join(os.path.abspath(outputdir), "{}.csv".format(lang)), index=False)


if __name__ == "__main__":
    if len(argv) != 3 or argv[1] == "--help" or argv[1] == "-h":
        print(merge_and_dump.__doc__)
    else:
        merge_and_dump(argv[1], argv[2])
