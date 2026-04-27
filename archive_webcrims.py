from archive import Archive

if __name__ == '__main__':
    archive = Archive()
    df = archive.create_dataframe()
    archive.save_to_archives(df=df)