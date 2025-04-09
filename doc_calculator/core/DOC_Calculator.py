from datetime import datetime
import pandas as pd
import numpy as np
import math

class DOC():
    def __init__(self, input_dict:dict) -> None:
        """
        ### Description
        This code enables to evaluate Direct and Total Operating Costs
        for Short/Medium haul airliners and regional aircraft (jet and
        propeller driven ).

        ### List of variables:
        - adp    (USD M)   Aircraft Delivery Price
        - htonn  (USD/T)   Coefficient of cost of handling per tonn


        - mtow  (Tonns)    Max Take-off Weight
        - pld   (Tonns)    Payload
        - mew   (Tonns)    Manufacturer Empty Weight
        - bengw (Tonns)    Bare engine weight
        - enpri (USD M)    Engine Price
        - en               Thermal Engines number
        - crewc            Attendants number
        - crewtech         Number of Tech. crew members (pilots)
        - bt      (HR)     Sector Block Time
        - bf      (KG)     Sector Block Fuel
        - sector  (NM)     Sector assumed for DOCs evaluation


        - ieng             Engine maintenance cost flag (1=Calculate, 2=Assigned in eoc parameter)
        - eoc    (USD/BHR) Engine overhaul cost (Necessary for ieng=2)
        - shp    (HP)      Thermal Engine Shaft Horse Power (Necessary for ieng=1)


        - afspare (fraction of adp)   Airframe spares in [0.0  1.0]
        - enspare (fraction of enpri) Spare engines and spares in [0.0  1.0]
        - dyrs    (YRS)               Depreciation period
        - rval                        Aircraft Residual value in [0.0  1.0]
        - rinsh   (fraction of adp)   Insurance rate in [0.0  1.0]
        - crtechr  (USD/BHR)          Tech. crew members (pilots) hourly tot.cost
        - crcabhr  (USD/BHR/Att )     Cab. crew member hourly cost
        - labor_rate       (USD/MHR)          Maintenance Labour rate
        - fuelpri  (USD/US GAL)       Fuel Price
        - ioc_fact                      Coeff. for IOC evaluation in [0.0  Inf)
        - util     (BHR/Annum)        Aircraft Annual Utilisation
        - lifespan                    Lifespan of the aircraft (years)
        - td       (EPNdB)            Departure airport threshold noise
        - ta       (EPNdB)            Arrival airport threshold noise
        - l_app (EPNdB)               Certified noise level at the approach measure point
        - l_lat (EPNdB)               Certified noise level at the lateral measure point
        - l_flyov (EPNdB)             Certified noise level at the fly-over measure point
        - cnoise  (USD)               Unit noise rate (Noise tariff that depends on the airport)


        - cnox     (USD)           Unit rate for NOX (generally referred to nitrogen oxides) (Emission tariff that depends on the airport)
        - nox_value (Kg)           Emission value of NOX. Equivalent of nitrogen oxide exhausted by an aircraft,
                                   in kilogram, in the "Landing and Take-Off Cycle, LTO
        - cco     (USD)            Unit rate for CO (generally referred to nitrogen oxides) (Emission tariff that depends on the airport)
        - co_value (Kg)            Emission value of CO. Equivalent of carbon monoxide exhausted by an aircraft, 
                                   in kilogram, in the "Landing and Take-Off Cycle, LTO
        - aec                      Portion of free Allocated Emission Certificate (tip: 0.15)
        - co2_value      (kg)      Mass of Emitted CO2, in kilograms
        - prico2   (USD/kg)        co2_value price for unit of emitted co2_value mass

        - n_bat                     Number of batteries pack     
        - NFC                      Number of fuel cells
        - NREPBAT                  Number of battery(ies) replacement during the aircraft lifespan
        - BATPRICE  (USD)          Battery(ies) price [USD]
        - RVBAT     (USD)          Battery(ies) residual value (at the end of its own life) [USD]
        - LRBAT     (USD/MMH)      Maintenance labor rate for battery(ies)
        - TLBAT     (MMH)          Maintenance man-hour for battery(ies) [hours]
        - FBAT                     Maintenance frequency for battery(ies) - as the reciprocal of the number of flights before the next check
        - NREPFC                   Number of fuel cell(s) replacement during the aircraft lifespan
        - FCPRICE   (USD)          Fuel Cell price [USD]
        - RVFC      (USD)          Fuel Cell(s) residual value (at the end of its own life) [USD]
        - LRFC      (USD/MMH)      Maintenance labor rate for fuel cell(s)
        - TLFC      (MMH)          Maintenance man-hour for fuel cell(s) [hours]
        - FFC                      Maintenance frequency for fuel cell(s) - as the reciprocal of the number of flights before the next check
        - NREPPE                   Number of power electronics replacement during the aircraft lifespan
        - PEPRICE   (USD)          Power electronics price [USD]
        - RVPE      (USD)          Power electronics residual value (at the end of its own life) [USD]
        - LRPE      (USD/MMH)      Maintenance labor rate for power electronics
        - TLPE      (MMH)          Maintenance man-hour for power electronics [hours]
        - FPE                      Maintenance frequency for power electronics - as the reciprocal of the number of flights before the next check

        - NEM                      Number of electric machines
        - EMPRICE   (USD)          Price of a single electric machine
        - LREM      (USD/MMH)      Maintenance labor rate for electric machine(s)
        - SPEML     (USD)          Spare Parts Cost Line Maintenance electric machine
        - SPEMB     (USD)          Spare Parts Cost Base Maintenance electric machine (If not known -> Assumption: SPEMB = 9.5*SPEML)
        - TLEML     (MMH)          Maintenance man-hour for line maintenance electric machine(s) [hours]
        - TLEMB     (MMH)          Maintenance man-hour for base maintenance electric machine(s) [hours]
        - FEML      (times/YR)     Maintenance frequency for electric machine(s) Line Maint.
        - FEMB      (times/BH)     Maintenance frequency for electric machine(s) Base Maint.

        - ENERPRI      (USD/kWh)   Electricity price 
        - ENERREQUIREMENT  (kWh)   Electricity Requirement (from battery)
        - H2PRI         (USD/kg)   H2 price
        - H2REQUIREMENT (kg)       H2 requirements
        
        """

        self.input_dict      = input_dict
        self.doc             = {} # DOC 
        self.ioc             = {} # IOC

        return None
    
    def calculate_doc(self) -> None:
        bt     = self.input_dict["bt"]
        pld    = self.input_dict["pld"]
        sector = self.input_dict["sector"]

        # Financial Costs [USD/BHR]
        self.doc["FINANCIAL [USD/BHR]"]      = self.__calculate_financial_cost()
        # Cash Operating Costs [USD/BHR]
        self.doc["CASH OPERATING [USD/BHR]"] = self.__calculate_cash_operating_cost()

        # DOC [USD/BHR]
        self.doc["DOC [USD/BHR]"] = self.doc["FINANCIAL [USD/BHR]"] + self.doc["CASH OPERATING [USD/BHR]"]
        # DOC [USD/trip]
        self.doc["DOC [USD/trip]"] = bt*self.doc["DOC [USD/BHR]"]

        return None
        
    def calculate_ioc(self) -> None:
        ioc_fact = self.input_dict["ioc_fact"]
        bt     = self.input_dict["bt"]

        # Cash Operating Costs [USD/BHR]
        cash_operating_cost = self.__calculate_cash_operating_cost()

        # Indirect Operating Costs [USD/BHR]
        self.ioc["IOC [USD/BHR]"] = ioc_fact*cash_operating_cost

        # Indirect Operating Costs [USD/trip]
        self.ioc["IOC [USD/trip]"] = bt*self.ioc["IOC [USD/BHR]"]

        return None
    
    def __calculate_cash_operating_cost(self) -> float:

        insurance                       = self.__calculate_insurance_cost()
        fuel                            = self.__calculate_fuel_cost()
        electric_energy                 = self.__calculate_electric_energy_price()
        h2                              = self.__calculate_h2_price()
        cockpit_crew                    = self.__calculate_cockpit_crew_cost()
        cabin_crew                      = self.__calculate_cabin_crew_cost()
        landing_fees                    = self.__calculate_landing_fees()
        nav_charges                     = self.__calculate_navigation_charges()
        ground_charges                  = self.__calculate_ground_handling_charges()
        noise_charges                   = self.__calculate_noise_charges()
        airframe_maintenance            = self.__calculate_airframe_maintenance_cost()
        thermal_engine_maintenance      = self.__calculate_thermal_engine_maintenance_cost()
        nox_emission_charges            = self.__calculate_nox_emission_charges()   
        co_emission_charges             = self.__calculate_co_emission_charges()   
        co2_emission_charges            = self.__calculate_co2_emission_charges()

        electric_machine_maint_line, electric_machine_maint_base    = self.__calculate_electric_machine_maintenance_cost()
        battery_maint_line, battery_maint_base                      = self.__calculate_battery_maintenance_cost()
        fuelcell_maint_line, fuelcell_maint_base                    = self.__calculate_fuel_cell_maintenance_cost()
        power_elec_maint_line, power_elec_maint_base                = self.__calculate_power_electronic_maintenance_cost() 

        self.doc["INSURANCE [USD/BHR]"]              = insurance
        self.doc["FUEL [USD/BHR]"]                   = fuel
        self.doc["ELECTRYCITY [USD/BHR]"]            = electric_energy
        self.doc["H2 [USD/BHR]"]                     = h2
        self.doc["COCKPIT CREW [USD/BHR]"]           = cockpit_crew
        self.doc["CABIN CREW [USD/BHR]"]             = cabin_crew
        self.doc["LANDING FEES [USD/BHR]"]           = landing_fees
        self.doc["NAVIGATION CHARGES [USD/BHR]"]     = nav_charges
        self.doc["GROUND HANDLING [USD/BHR]"]        = ground_charges
        self.doc["NOISE CHARGES [USD/BHR]"]          = noise_charges
        self.doc["NOX EMISSION CHARGES [USD/BHR]"]   = nox_emission_charges
        self.doc["CO EMISSION CHARGES [USD/BHR]"]    = co_emission_charges
        self.doc["co2_value EMISSION CHARGES [USD/BHR]"]   = co2_emission_charges
        self.doc["AIRFRANE MAINTENANCE [USD/BHR]"]   = airframe_maintenance
        self.doc["THERM. ENG. MAINTENANCE [USD/BH]"] = thermal_engine_maintenance

        self.doc["ELECTRIC MACHINE LINE MAINT. [USD/BH]"] = electric_machine_maint_line
        self.doc["ELECTRIC MACHINE BASE MAINT. [USD/BH]"] = electric_machine_maint_base
        self.doc["BATTERY LINE MAINT. [USD/BH]"]          = battery_maint_line 
        self.doc["BATTERY BASE MAINT. [USD/BH]"]          = battery_maint_base
        self.doc["FUEL CELL LINE MAINT. [USD/BH]"]        = fuelcell_maint_line 
        self.doc["FUEL CELL BASE MAINT. [USD/BH]"]        = fuelcell_maint_base 
        self.doc["POWER ELECTR. LINE MAINT. [USD/BH]"]    = power_elec_maint_line 
        self.doc["POWER ELECTR. BASE MAINT. [USD/BH]"]    = power_elec_maint_base 


        cash_operating_cost_list = [insurance, fuel, electric_energy, h2, cockpit_crew, cabin_crew, thermal_engine_maintenance, airframe_maintenance, 
            landing_fees, nav_charges, ground_charges, noise_charges, nox_emission_charges, co_emission_charges, co2_emission_charges,
            electric_machine_maint_line, electric_machine_maint_base, battery_maint_line, battery_maint_base, fuelcell_maint_line, fuelcell_maint_base,
            power_elec_maint_line, power_elec_maint_base]        

        cash_operating_cost = np.sum(cash_operating_cost_list)
        return cash_operating_cost
    
    def __calculate_financial_cost(self) -> float:

        depr     = self.__calculate_depreciation()
        interest = self.__calculate_interest()

        self.doc["DEPRECIATION [USD/BHR]"] = depr
        self.doc["INTEREST [USD/BHR]"]     = interest

        financial = depr + interest
        return financial
    
    def __calculate_co2_emission_charges(self) -> float:
        aec    = self.input_dict["aec"]   # portion of free Allocated Emission Certificate (0.15]
        co2_value    = self.input_dict["co2_value"]    # mass of co2_value [kg]
        prico2 = self.input_dict["prico2"] # unitary price of co2_value emitted [USD/kg]
        bt     = self.input_dict["bt"] 

        co2_emission_charges = (1.0-aec)*co2_value*prico2/bt
        return co2_emission_charges
    
    def __calculate_battery_maintenance_cost(self) -> tuple[float, float]:
        n_bat     = self.input_dict["n_bat"]
        NREPBAT  = self.input_dict["NREPBAT"]
        BATPRICE = self.input_dict["BATPRICE"]
        RVBAT    = self.input_dict["RVBAT"]
        LRBAT    = self.input_dict["LRBAT"]
        TLBAT    = self.input_dict["TLBAT"]
        FBAT     = self.input_dict["FBAT"]
        lifespan = self.input_dict["lifespan"]
        util     = self.input_dict["util"]

        battery_maint_line = n_bat*LRBAT*TLBAT*FBAT
        battery_maint_base = n_bat*(NREPBAT*(BATPRICE-RVBAT))/(lifespan*util) # replace
        return battery_maint_line, battery_maint_base
    
    def __calculate_fuel_cell_maintenance_cost(self) -> tuple[float, float]:
        NFC      = self.input_dict["NFC"]
        NREPFC   = self.input_dict["NREPFC"]
        FCPRICE  = self.input_dict["FCPRICE"]
        RVFC     = self.input_dict["RVFC"]
        LRFC     = self.input_dict["LRFC"]
        TLFC     = self.input_dict["TLFC"]
        FFC      = self.input_dict["FFC"]
        lifespan = self.input_dict["lifespan"]
        util     = self.input_dict["util"]

        fuel_cell_maint_line = NFC*LRFC*TLFC*FFC
        fuel_cell_maint_base = NFC*(NREPFC*(FCPRICE-RVFC))/(lifespan*util) # replace
        return fuel_cell_maint_line, fuel_cell_maint_base
    
    def __calculate_power_electronic_maintenance_cost(self) -> tuple[float, float]:
        NREPPE   = self.input_dict["NREPPE"]
        PEPRICE  = self.input_dict["PEPRICE"]
        RVPE     = self.input_dict["RVPE"]
        LRPE     = self.input_dict["LRPE"]
        TLPE     = self.input_dict["TLPE"]
        FPE      = self.input_dict["FPE"]
        lifespan = self.input_dict["lifespan"]
        util     = self.input_dict["util"]

        power_electronic_maint_line = LRPE*TLPE*FPE
        power_electronic_maint_base = (NREPPE*(PEPRICE-RVPE))/(lifespan*util) # replace
        return power_electronic_maint_line, power_electronic_maint_base

    def __calculate_electric_machine_maintenance_cost(self) -> tuple[float, float]:
        NEM      = self.input_dict["NEM"]     
        SPEML    = self.input_dict["SPEML"]       # spare parts cost line maintenance
        SPEMB    = self.input_dict["SPEMB"]       # spare parts cost base maintenance
        LREM     = self.input_dict["LREM"]
        TLEML    = self.input_dict["TLEML"]       # maintenance man hour line maint.
        TLEMB    = self.input_dict["TLEMB"]       # maintenance man hour base maint.
        FEML     = self.input_dict["FEML"]        # maintenance frequency line maint
        FEMB     = self.input_dict["FEMB"]        # maintenance frequency base maint
        lifespan = self.input_dict["lifespan"]
        util     = self.input_dict["util"]
        
        electric_machine_maint_line = NEM*(SPEML + LREM*TLEML)*lifespan*FEML/util
        electric_machine_maint_base = NEM*(SPEMB + LREM*TLEMB)*FEMB*0.80
        return electric_machine_maint_line, electric_machine_maint_base
    
    def __calculate_airframe_maintenance_cost(self) -> float:
        n_bat      = self.input_dict["n_bat"]         
        NEM       = self.input_dict["NEM"]
        NFC       = self.input_dict["NFC"]
        BATPRICE  = self.input_dict["BATPRICE"]
        FCPRICE   = self.input_dict["FCPRICE"]
        EMPRICE   = self.input_dict["EMPRICE"]
        bt        = self.input_dict["bt"]
        adp       = self.input_dict["adp"]
        en        = self.input_dict["en"]
        enpri     = self.input_dict["enpri"]
        mew       = self.input_dict["mew"]
        bengw     = self.input_dict["bengw"]
        labor_rate        = self.input_dict["labor_rate"]

        M   = 1.0 # Mach Number (Assumed 1 for subsonic cruise)
        FT  = bt - 0.25
        AFW = mew-(bengw*en)

        C_A_FH = 3.08*(adp - en*enpri - n_bat*BATPRICE/1.0e6 - NEM*EMPRICE/1.0e6 - NFC*FCPRICE/1.0e6)
        C_A_FC = 6.24*(adp - en*enpri - n_bat*BATPRICE/1.0e6 - NEM*EMPRICE/1.0e6 - NFC*FCPRICE/1.0e6)
        K_A_FC = 0.05*AFW*2.2 + 6 - 630.0/(AFW*2.2 + 120.0)
        K_A_FH = 0.59*K_A_FC
        
        airframe_labor_cost    = (K_A_FH*FT + K_A_FC)*labor_rate*math.sqrt(M)/bt
        airframe_material_cost = (C_A_FH*FT + C_A_FC)/bt

        airframe_maintenance_cost = airframe_material_cost + airframe_labor_cost
        return airframe_maintenance_cost

    def __calculate_thermal_engine_maintenance_cost(self) -> float:
        ieng = self.input_dict["ieng"]
        en   = self.input_dict["en"]
        
        if ieng == 1:
            bt    = self.input_dict["bt"]
            labor_rate    = self.input_dict["labor_rate"]
            shp   = self.input_dict["shp"]
            enpri = self.input_dict["enpri"]

            FT       = bt - 0.25
            K_ICE_FC = (0.3 + 0.03*shp/1000.0)*en
            K_ICE_FH = (0.65 + 0.03*shp/1000.0)*en
            C_ICE_FC = 2.0*en*enpri*10.0
            C_ICE_FH = 2.5*en*enpri*10.0

            thermal_engine_labor_cost    = (K_ICE_FH*FT + K_ICE_FC)*labor_rate/bt
            thermal_engine_material_cost = (C_ICE_FH*FT + C_ICE_FC)/bt

            thermal_engine_maintenance_cost = thermal_engine_material_cost + thermal_engine_labor_cost

        elif ieng == 2:
            eoc = self.input_dict["eoc"]

            thermal_engine_maintenance_cost = eoc*en
            
        else:
            raise ValueError(f"ieng Value {ieng} not valid")
        
        return thermal_engine_maintenance_cost
    
    def __calculate_nox_emission_charges(self) -> float:
        cnox        = self.input_dict["cnox"]
        nox_value = self.input_dict["nox_value"]
        bt           = self.input_dict["bt"]

        nox_emission_charges = (cnox*nox_value)/bt
        return nox_emission_charges

    def __calculate_co_emission_charges(self) -> float:
        cco         = self.input_dict["cco"]
        co_value  = self.input_dict["co_value"]
        bt           = self.input_dict["bt"]

        co_emission_charges  = (cco*co_value)/bt
        return co_emission_charges
    
    def __calculate_noise_charges(self) -> float:
        l_app   = self.input_dict["l_app"]
        ta      = self.input_dict["ta"]
        l_flyov = self.input_dict["l_flyov"]
        l_lat   = self.input_dict["l_lat"]
        td      = self.input_dict["td"]
        bt      = self.input_dict["bt"]
        cnoise  = self.input_dict["cnoise"]

        DELTAA = (l_app-ta)/10.0
        DELTAD = (((l_flyov+l_lat)/2.0)-td)/10.0
        
        noise_charges = (cnoise*(10.0**(DELTAA)+10.0**(DELTAD)))/bt
        return noise_charges

    def __calculate_ground_handling_charges(self) -> float:
        htonn = self.input_dict["htonn"]
        pld   = self.input_dict["pld"]
        bt    = self.input_dict["bt"]

        ground_charges = (htonn*pld)/bt
        return ground_charges
    
    def __calculate_navigation_charges(self) -> float:
        mtow   = self.input_dict["mtow"]
        bt     = self.input_dict["bt"]
        sector = self.input_dict["sector"]

        nav_charges = (68.5*sector*1.853/100.0)*math.sqrt(mtow/50.0)/bt
        return nav_charges
    
    def __calculate_landing_fees(self) -> float:
        mtow = self.input_dict["mtow"]
        bt   = self.input_dict["bt"]

        landing_fees = (10.0*mtow)/bt
        return landing_fees

    def __calculate_cabin_crew_cost(self) -> float:
        crcabhr = self.input_dict["crcabhr"]
        crewc   = self.input_dict["crewc"]

        cabin_crew = crcabhr*crewc
        return cabin_crew
    
    def __calculate_cockpit_crew_cost(self) -> float:
        crtechr  = self.input_dict["crtechr"]
        crewtech = self.input_dict["crewtech"]

        cockpit_crew = crtechr*crewtech
        return cockpit_crew
    
    def __calculate_h2_price(self) -> None:
        H2PRI         = self.input_dict["H2PRI"]
        H2REQUIREMENT = self.input_dict["H2REQUIREMENT"]
        bt            = self.input_dict["bt"]

        h2_price = H2PRI*H2REQUIREMENT/bt
        return h2_price
    
    def __calculate_electric_energy_price(self) -> None:
        ENERPRI         = self.input_dict["ENERPRI"]
        ENERREQUIREMENT = self.input_dict["ENERREQUIREMENT"]
        bt              = self.input_dict["bt"]

        electric_energy_price = ENERREQUIREMENT*ENERPRI/bt
        return electric_energy_price
    
    def __calculate_fuel_cost(self) -> float:
        fuelpri = self.input_dict["fuelpri"]
        bf      = self.input_dict["bf"]
        bt      = self.input_dict["bt"]

        fuel = (0.328*fuelpri*bf)/bt
        return fuel
    
    def __calculate_insurance_cost(self) -> float:
        rinsh = self.input_dict["rinsh"]
        adp   = self.input_dict["adp"]*1.0e6
        util  = self.input_dict["util"]

        insurance = (rinsh*adp)/util
        return insurance
    
    def __calculate_investment(self) -> float:
        adp     = self.input_dict["adp"]*1.0e6
        afspare = self.input_dict["afspare"]
        enpri   = self.input_dict["enpri"]
        en      = self.input_dict["en"]
        enspare = self.input_dict["enspare"]

        invest = adp+(afspare*(adp-enpri*en))+(enspare*enpri*en)
        return invest
    
    def __calculate_interest(self) -> float:
        util = self.input_dict["util"]

        INVEST = self.__calculate_investment()
        
        interest = (0.053*INVEST)/util
        return interest
        
    def __calculate_depreciation(self) -> float:
        rval   = self.input_dict["rval"]
        dyrs   = self.input_dict["dyrs"]
        util   = self.input_dict["util"]

        INVEST = self.__calculate_investment()

        depr = ((1-rval)*INVEST)/(dyrs*util)
        return depr