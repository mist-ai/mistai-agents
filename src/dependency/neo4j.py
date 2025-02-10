from neo4j import GraphDatabase

# Neo4j connection details
URI = "bolt://localhost:7687"  # Update if necessary
USER = "neo4j"
PASSWORD = "password"

# Your data
data = {
    "Automobiles & Components": {"Kelani Tyres": "TYRE.N0000"},
    "Banks": {
        "Amana Bank PLC": "ABL.N0000",
        "Cargills Bank Limited": "CBNK.N0000",
        "Commercial Bank of Ceylon PLC": "COMB.N0000",
        "DFCC Bank PLC": "DFCC.N0000",
        "Hatton National Bank PLC": "HNB.N0000",
        "Housing Development Finance Corporation Bank of Sri Lanka": "HDFC.N0000",
        "National Development Bank PLC": "NDB.N0000",
        "Nations Trust Bank PLC": "NTB.N0000",
        "Pan Asia Banking Corporation PLC": "PABC.N0000",
        "Sampath Bank PLC": "SAMP.N0000",
        "SANASA Development Bank PLC": "SDB.N0000",
        "Seylan Bank PLC": "SEYB.N0000",
        "Union Bank of Colombo PLC": "UBC.N0000",
    },
    "Capital Goods": {
        "Access Engineering PLC": "AEL.N0000",
        "ACL Cables PLC": "ACL.N0000",
        "Aitken Spence PLC": "SPEN.N0000",
        "Central Industries PLC": "CIND.N0000",
        "E.B. Creasy & Company PLC": "EBCR.N0000",
        "Hayleys PLC": "HAYL.N0000",
        "Hemas Holdings PLC": "HHL.N0000",
        "John Keells Holdings PLC": "JKH.N0000",
        "Kelani Cables PLC": "KCAB.N0000",
        "Lanka Ashok Leyland PLC": "LALU.N0000",
        "Lanka Tiles PLC": "TILE.N0000",
        "Lanka Walltiles PLC": "LWL.N0000",
        "Laxapana Batteries PLC": "LAXA.N0000",
        "Renuka Holdings PLC": "RHL.N0000",
        "Richard Pieris and Company PLC": "RICH.N0000",
        "Royal Ceramics Lanka PLC": "RCL.N0000",
        "Sierra Cables PLC": "SIRA.N0000",
        "The Colombo Fort Land & Building PLC": "CFLB.N0000",
    },
    "Office Equipment": {
        "Alpha Fire Services Limited": "AFS.N0000",
        "Brown and Company PLC": "BRWN.N0000",
        "Cable Solutions (Private) Limited": "CSLK.N0000",
        "Greentech Energy Systems Limited": "MEL.N0000",
        "Lanka Ceramic PLC": "CERA.N0000",
        "Lankem Ceylon PLC": "LCEY.N0000",
        "Luminex PLC": "LUMX.N0000",
        "Vallibel One PLC": "VONE.N0000",
        "Colombo Dockyard PLC": "DOCK.N0000",
        "Serendib Engineering Group PLC": "IDL.N0000",
        "Softlogic Holdings PLC": "SHL.N0000",
    },
    "Commercial & Professional Services": {
        "Gestetner of Ceylon PLC": "GEST.N0000",
        "Lake House Printers & Publishers PLC": "LPRT.N0000",
        "Printcare PLC": "CARE.N0000",
        "Ceylon Printers PLC": "CPRT.N0000",
        "Paragon Ceylon PLC": "PARQ.N0000",
        "E M L Consultants Limited": "EML.N0000",
    },
    "Consumer Durables & Apparel": {
        "Abans Electricals PLC": "ABAN.N0000",
        "Hayleys Fabric PLC": "MGT.N0000",
        "Hayleys Fibre PLC": "HEXP.N0000",
        "Hela Apparel Holdings PLC": "HELA.N0000",
        "Radiant Gems International PLC": "RGEM.N0000",
        "Teejay Lanka PLC": "TJL.N0000",
        "Ambeon Capital PLC": "TAP.N0000",
        "Ambeon Holdings PLC": "GREG.N0000",
        "Dankotuwa Porcelain PLC": "DPL.N0000",
        "Blue Diamonds Jewellery Worldwide PLC": "BLUE.N0000",
        "Kelsey Developments PLC": "KDL.N0000",
    },
    "Consumer Services": {
        "Aitken Spence Hotel Holdings PLC": "AHUN.N0000",
        "Asian Hotels and Properties PLC": "AHPL.N0000",
        "Ceylon Hotels Corporation PLC": "CHOT.N0000",
        "Citrus Leisure PLC": "REEF.N0000",
        "Dolphin Hotels PLC": "DOLP.N0000",
        "Hayleys Leisure PLC": "CONN.N0000",
        "Hotel Sigiriya PLC": "HSIG.N0000",
        "Renuka City Hotel PLC": "RECH.N0000",
        "Sigiriya Village Hotels PLC": "SVIL.N0000",
        "Tangerine Beach Hotels PLC": "TANG.N0000",
        "The Kingsbury PLC": "SERV.N0000",
        "Eden Hotel Lanka PLC": "EDEN.N0000",
        "Hunas Holdings PLC": "HUNA.N0000",
        "Palm Garden Hotels PLC": "PALM.N0000",
        "Kandy Hotels Company (1938) PLC": "KHC.N0000",
        "Trans Asia Hotels PLC": "TRAN.N0000",
        "Bansei Resorts Company PLC": "BERU.N0000",
        "Beruwala Resorts PLC": "BRR.N0000",
        "Galadari Hotels (Lanka) PLC": "GHLL.N0000",
        "Citrus Hikkaduwa PLC": "CITR.N0000",
        "Jetwing Symphony PLC": "JETS.N0000",
        "John Keells Hotels PLC": "KHL.N0000",
        "Mahaweli Reach Hotels PLC": "MRH.N0000",
        "Marawila Resorts PLC": "MAR.N0000",
        "Pegasus Hotels of Ceylon PLC": "PEG.N0000",
        "Ramboda Falls PLC": "RAL.N0000",
        "Renuka Hotels PLC": "RHL.N0000",
        "Royal Palms Beach Hotels PLC": "RPBH.N0000",
        "Serendib Hotels PLC": "SHOT.N0000",
        "Taj Lanka Hotels PLC": "TAJ.N0000",
        "The Lighthouse Hotel PLC": "LHL.N0000",
        "The Fortress Resorts PLC": "FORT.N0000",
        "Nuwara Eliya Hotels Company PLC": "NEH.N0000",
        "Citrus Waskaduwa PLC": "CITW.N0000",
    },
    "Diversified Financials": {
        "Alliance Finance Company PLC": "ALLI.N0000",
        "Asia Asset Finance PLC": "AAF.N0000",
        "Central Finance Company PLC": "CFIN.N0000",
        "Ceylon Guardian Investment Trust PLC": "GUAR.N0000",
        "Ceylon Investment PLC": "CINV.N0000",
        "Ceylon Land PLC": "CLND.N0000",
        "Citizens Development Business Finance PLC": "CDB.N0000",
        "Galle Face Capital Partners PLC": "GFC.N0000",
        "Lanka Orix Leasing Company PLC": "LOLC.N0000",
        "Lanka Ventures PLC": "LVEN.N0000",
        "LB Finance PLC": "LFIN.N0000",
        "People's Leasing & Finance PLC": "PLC.N0000",
        "Singer Finance (Lanka) PLC": "SFIN.N0000",
        "Vallibel Finance PLC": "VFIN.N0000",
        "Abans Finance PLC": "AFSL.N0000",
        "Capital Alliance Limited": "CALT.N0000",
        "Dialog Finance PLC": "CALF.N0000",
        "LOLC Finance PLC": "LOFC.N0000",
        "Mercantile Investments and Finance PLC": "MERC.N0000",
        "Orient Finance PLC": "BFN.N0000",
        "Softlogic Finance PLC": "CRL.N0000",
        "Asia Siyaka Commodities PLC": "ASIY.N0000",
        "Associated Motor Finance Company PLC": "AMF.N0000",
        "Capital Alliance Treasury Limited": "CALT.N0000",
        "Central Finance Company PLC": "CFIN.N0000",
        "Citizens Development Business Finance PLC": "CDB.N0000",
        "Commercial Credit & Finance PLC": "COCR.N0000",
        "First Capital Holdings PLC": "CFVF.N0000",
        "First Capital Treasuries PLC": "FCT.N0000",
        "HNB Finance PLC": "HNBF.N0000",
        "Lanka Credit and Business Finance PLC": "LCBF.N0000",
        "Merchant Bank of Sri Lanka & Finance PLC": "MBSL.N0000",
        "People's Merchant Finance PLC": "PMB.N0000",
        "Senkadagala Finance PLC": "SFCL.N0000",
        "UB Finance Company Limited": "UBF.N0000",
        "Asia Capital PLC": "ACAP.N0000",
        "Bimputh Finance PLC": "BLI.N0000",
        "Nation Lanka Finance PLC": "CSF.N0000",
    },
    "Energy": {"Lanka IOC PLC": "LIOC.N0000", "LAUGFS Gas PLC": "LGL.N0000"},
    "Food & Staples Retailing": {
        "C T Holdings PLC": "CTHR.N0000",
        "Cargills (Ceylon) PLC": "CARG.N0000",
        "Tess Agro PLC": "TESS.N0000",
    },
    "Food, Beverage & Tobacco": {
        "Agalawatte Plantations PLC": "AGAL.N0000",
        "Balaha Farms PLC": "BALF.N0000",
        "Balangoda Plantations PLC": "BALA.N0000",
        "Bukit Darah PLC": "BUKI.N0000",
        "Carson Cumberbatch PLC": "CARS.N0000",
        "Ceylon Cold Stores PLC": "CCS.N0000",
        "Ceylon Grain Elevators PLC": "GRAN.N0000",
        "Ceylon Tobacco Company PLC": "CTC.N0000",
        "Convenience Foods (Lanka) PLC": "SOY.N0000",
        "Horana Plantations PLC": "HOPL.N0000",
        "Kegalle Plantations PLC": "KGAL.N0000",
        "Kotagala Plantations PLC": "KOTA.N0000",
        "Lanka Milk Foods (CWE) PLC": "LMF.N0000",
        "Lankem Developments PLC": "LDEV.N0000",
        "Lion Brewery (Ceylon) PLC": "LION.N0000",
        "Malwatte Valley Plantations PLC": "MAL.N0000",
        "Melstacorp PLC": "MELS.N0000",
        "Namunukula Plantations PLC": "NAMU.N0000",
        "Renuka Agri Foods PLC": "RAL.N0000",
        "Renuka Foods PLC": "COCO.N0000",
        "Sunshine Holdings PLC": "SUN.N0000",
        "Talawakelle Tea Estates PLC": "TALA.N0000",
        "Tea Smallholder Factories PLC": "TSML.N0000",
        "Three Acre Farms PLC": "TAFL.N0000",
        "Watawala Plantations PLC": "WATA.N0000",
        "Aitken Spence Plantation Managements PLC": "SPEN.N0000",
        "Distilleries Company of Sri Lanka PLC": "DIST.N0000",
        "Hapugastenne Plantations PLC": "HAPU.N0000",
        "Kotmale Holdings PLC": "KOTA.N0000",
        "Madulsima Plantations PLC": "MADU.N0000",
        "Udapussellawa Plantations PLC": "UDPL.N0000",
        "Maharaja Foods (Private) Limited": "MFPE.N0000",
        "Agarapatana Plantations Limited": "AGPL.N0000",
        "Bogawantalawa Tea Estates PLC": "BOPL.N0000",
        "Browns Investments PLC": "BIL.N0000",
        "Ceylon Beverage Holdings PLC": "BREW.N0000",
        "Dilmah Ceylon Tea Company PLC": "CTEA.N0000",
        "Elpitiya Plantations PLC": "ELPL.N0000",
        "Harischandra Mills PLC": "HARI.N0000",
        "Hatton Plantations PLC": "HPL.N0000",
        "HVA Foods PLC": "HVA.N0000",
        "Kahawatte Plantations PLC": "KAHA.N0000",
        "Keells Food Products PLC": "KFP.N0000",
        "Mahaweli Coconut Plantations Limited": "MCPL.N0000",
        "Maskeliya Plantations PLC": "MASK.N0000",
        "Raigam Wayamba Salterns PLC": "RWSL.N0000",
    },
    "Health Care Equipment & Services": {
        "CEYLON HOSPITALS PLC (DURDANS)": "CHL.N0000",
        "MULLER & PHIPPS (CEYLON) PLC": "MULL.N0000",
        "NAWALOKA HOSPITALS PLC": "NHL.N0000",
        "THE LANKA HOSPITALS CORPORATION PLC": "LHCL.N0000",
        "E-CHANNELLING PLC": "ECL.N0000",
        "SINGHE HOSPITALS PLC": "SINH.N0000",
        "ASIRI HOSPITAL HOLDINGS PLC": "ASIR.N0000",
        "ASIRI SURGICAL HOSPITAL PLC": "AMSL.N0000",
    },
    "Household & Personal Products": {
        "BPPL HOLDINGS": "BPPL.N0000",
        "SWADESHI INDUSTRIAL WORKS PLC": "SWAD.N0000",
    },
    "Insurance": {
        "CEYLINCO HOLDINGS": "CEY.N0000",
        "HNB ASSURANCE": "HNB.N0000",
        "PEOPLES INSURANCE": "PINS.N0000",
        "AMANA TAKAFUL LIFE PLC": "ATLL.N0000",
        "AMANA TAKAFUL PLC": "ATL.N0000",
        "ARPICO INSURANCE": "ARP.N0000",
        "Co-operative Insurance Company PLC": "COOP.N0000",
        "JANASHAKTHI INSURANCE": "JINS.N0000",
        "LOLC GENERAL INSURANCE": "LOLC.N0000",
        "SOFTLOGIC CAPITAL PLC": "SCAP.N0000",
        "SOFTLOGIC LIFE INSURANCE PLC": "AAIC.N0000",
        "UNION ASSURANCE PLC": "UAL.N0000",
    },
    "Materials": {
        "ACL PLASTICS PLC": "APLA.N0000",
        "C I C HOLDINGS PLC": "CIC.N0000",
        "CHEMANEX PLC": "CHMX.N0000",
        "CHEVRON LUBRICANTS LANKA PLC": "LLUB.N0000",
        "DIPPED PRODUCTS": "DPL.N0000",
        "EX-PACK": "EXPO.N0000",
        "HAYCARB": "HAYC.N0000",
        "INDUSTRIAL ASPHALTS (CEYLON) PLC": "ASPH.N0000",
        "LANKA ALUMINIUM": "LALU.N0000",
        "PGP GLASS": "PGP.N0000",
        "SAMSON INTERNATIONAL": "SAM.N0000",
        "SWISSTEK (CEYLON) PLC": "PARQ.N0000",
        "TOKYO CEMENT": "TCL.N0000",
        "UNION CHEMICALS LANKA PLC": "UCAR.N0000",
        "JAT HOLDINGS": "JAT.N0000",
        "AGSTAR PLC": "AGST.N0000",
        "ALUMEX PLC": "ALUM.N0000",
        "BOGALA GRAPHITE": "BOGA.N0000",
        "RICHARD PIERIS EXPORTS PLCT": "REXP.N0000",
        "ACME PRINTING & PACKAGING PLC": "ACME.N0000",
    },
    "Real Estate Management & Development": {
        "CARGO BOAT DEVELOPMENT COMPANY PLC": "CBOA.N0000",
        "COLOMBO CITY HOLDINGS PLC": "None",
        "COLOMBO LAND AND DEVELOPMENT COMPANY PLC": "CLND.N0000",
        "EAST WEST PROPERTIES PLC": "EAST.N0000",
        "LANKA REALTY INVESTMENTS PLC": "ASCO.N0000",
        "LEE HEDGES PLC": "SHAW.N0000",
        "SEYLAN DEVELOPMENTS PLC": "CSD.N0000",
        "YORK ARCADE HOLDINGS PLC": "YORK.N0000",
    },
    "Retailing": {
        "C M HOLDINGS PLC": "COLO.N0000",
        "DIESEL & MOTOR ENGINEERING PLC": "DIMO.N0000",
        "EASTERN MERCHANTS PLC": "EMER.N0000",
        "HUNTER & COMPANY PLC": "HUNT.N0000",
        "KAPRUKA HOLDINGS PLC": "KPHL.N0000",
        "R I L PROPERTY PLC": "RIL.N0000",
        "THE AUTODROME PLC": "AUTO.N0000",
        "UNITED MOTORS LANKA PLC": "UML.N0000",
        "SINGER (SRI LANKA) PLC": "SINS.N0000",
        "C. W. MACKIE PLC": "CWM.N0000",
        "CEYLON TEA BROKERS PLC": "CTBL.N0000",
        "JOHN KEELLS HOLDINGS PLC": "JKH.N0000",
        "SATHOSA MOTORS PLC": "SMOT.N0000",
        "ODEL PLC": "ODEL.N0000",
    },
    "Software & Services": {"hSenid Business Solutions PLC": "HBS.N0000"},
    "Telecommunication Services": {
        "DIALOG AXIATA PLC": "DIAL.N0000",
        "SRI LANKA TELECOM PLC": "SLT.N0000",
    },
    "Utilities": {
        "Lanka Electricity Company": "LECO.N0000",
        "LAUGFS POWER PLC": "LPL.N0000",
        "VIDULLANKA PLC": "VLL.N0000",
        "VALLIBEL POWER ERATHNA PLC": "VPEL.N0000",
        "RESUS ENERGY PLCy": "HPWR.N0000",
        "PANASIAN POWER PLC": "PAN.N0000",
        "LOTUS HYDRO POWER PLC": "HPFL.N0000",
    },
}


# Neo4j driver
class Neo4jHandler:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.driver.verify_connectivity()

    def close(self):
        self.driver.close()

    def save_data(self, data):
        with self.driver.session() as session:
            for sector, companies in data.items():
                # Create sector node
                session.write_transaction(self.create_sector, sector)

                for company, ticker in companies.items():
                    session.write_transaction(self.create_company, company, ticker)
                    session.write_transaction(self.create_relationship, company, sector)

    @staticmethod
    def create_sector(tx, sector_name):
        query = """
        MERGE (s:Sector {name: $sector_name})
        """
        tx.run(query, sector_name=sector_name)

    @staticmethod
    def create_company(tx, company_name, ticker):
        query = """
        MERGE (c:Company {name: $company_name})
        SET c.ticker = $ticker
        """
        tx.run(query, company_name=company_name, ticker=ticker)

    @staticmethod
    def create_relationship(tx, company_name, sector_name):
        query = """
        MATCH (c:Company {name: $company_name})
        MATCH (s:Sector {name: $sector_name})
        MERGE (c)-[:BELONGS_TO]->(s)
        """
        tx.run(query, company_name=company_name, sector_name=sector_name)


# Run the script
neo4j_handler = Neo4jHandler(URI, USER, PASSWORD)
neo4j_handler.save_data(data)
neo4j_handler.close()

print("Data successfully saved to Neo4j!")
