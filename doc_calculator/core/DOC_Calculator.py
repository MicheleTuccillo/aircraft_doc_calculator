from doc_calculator.core.utils.util_functions import _assign_input
from doc_calculator.core.utils.params import Params 
import numpy as np
import math

class DOC():
    def __init__(self, aircraft:dict, params:Params=Params()) -> None:
        """
        ### Description
        This code enables to evaluate Direct and Total Operating Costs
        for Short/Medium haul airliners and regional aircraft (jet and
        propeller driven ).

        ### Input Dict Keys
        List of variables composing the aircraft dict (case insensitive):
        - adp    (USD M)   Aircraft Delivery Price

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
        - labor_rate       (USD/MHR)  Maintenance Labour rate
        - fuelpri  (USD/US GAL)       Fuel Price
        - ioc_fact                    Coeff. for IOC evaluation in [0.0  Inf)
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
        - co2_value      (kg)      Mass of Emitted CO2, in kilograms
        - prico2   (USD/kg)        co2_value price for unit of emitted co2_value mass

        - n_bat                    Number of batteries pack     
        - n_fc                     Number of fuel cells
        - n_repbat                 Number of battery(ies) replacement during the aircraft lifespan
        - batprice  (USD)          Battery(ies) price [USD]
        - rvbat     (USD)          Battery(ies) residual value (at the end of its own life) [USD]
        - lrbat     (USD/MMH)      Maintenance labor rate for battery(ies)
        - tlbat     (MMH)          Maintenance man-hour for battery(ies) [hours]
        - f_bat                    Maintenance frequency for battery(ies) - as the reciprocal of the number of flights before the next check
        - n_repfc                  Number of fuel cell(s) replacement during the aircraft lifespan
        - fcprice   (USD)          Fuel Cell price [USD]
        - rvfc      (USD)          Fuel Cell(s) residual value (at the end of its own life) [USD]
        - lrfc      (USD/MMH)      Maintenance labor rate for fuel cell(s)
        - tlfc      (MMH)          Maintenance man-hour for fuel cell(s) [hours]
        - f_fc                     Maintenance frequency for fuel cell(s) - as the reciprocal of the number of flights before the next check
        - n_reppe                  Number of power electronics replacement during the aircraft lifespan
        - peprice   (USD)          Power electronics price [USD]
        - rvpe      (USD)          Power electronics residual value (at the end of its own life) [USD]
        - lrpe      (USD/MMH)      Maintenance labor rate for power electronics
        - tlpe      (MMH)          Maintenance man-hour for power electronics [hours]
        - f_pe                     Maintenance frequency for power electronics - as the reciprocal of the number of flights before the next check

        - n_em                     Number of electric machines
        - emprice   (USD)          Price of a single electric machine
        - lrem      (USD/MMH)      Maintenance labor rate for electric machine(s)
        - speml     (USD)          Spare Parts Cost Line Maintenance electric machine
        - spemb     (USD)          Spare Parts Cost Base Maintenance electric machine (If not known -> Assumption: spemb = 9.5*speml)
        - tleml     (MMH)          Maintenance man-hour for line maintenance electric machine(s) [hours]
        - tlemb     (MMH)          Maintenance man-hour for base maintenance electric machine(s) [hours]
        - f_eml      (times/YR)    Maintenance frequency for electric machine(s) Line Maint.
        - f_emb      (times/BH)    Maintenance frequency for electric machine(s) Base Maint.

        - enerpri      (USD/kWh)   Electricity price 
        - ener_req  (kWh)          Electricity Requirement (from battery)
        - h2_pri         (USD/kg)  H2 price
        - h2_req (kg)              H2 requirements
        
        """
        self.aircraft = _assign_input(input=aircraft)
        self.__params   = params

        return None
    
    def calculate_doc(self) -> dict:
        bt = self.aircraft["bt"]

        doc = {}

        # Financial Costs [USD/BHR]
        financial_costs = self.__calculate_financial_cost()

        # Cash Operating Costs [USD/BHR]
        cash_operating_costs = self.__calculate_cash_operating_cost()

        # DOC [USD/BHR]
        doc = {**financial_costs, **cash_operating_costs}
        doc["DOC [USD/BHR]"] = sum(financial_costs.values()) + sum(cash_operating_costs.values())

        # DOC [USD/flight]
        doc["DOC [USD/flight]"] = bt*doc["DOC [USD/BHR]"]

        return doc
        
    def calculate_ioc(self) -> dict:
        ioc_fact = self.aircraft["ioc_fact"]
        bt     = self.aircraft["bt"]

        ioc = {}

        # Cash Operating Costs [USD/BHR]
        cash_operating_cost = self.__calculate_cash_operating_cost()

        # Indirect Operating Costs [USD/BHR]
        ioc["IOC [USD/BHR]"] = ioc_fact*sum(cash_operating_cost.values())

        # Indirect Operating Costs [USD/flight]
        ioc["IOC [USD/flight]"] = bt*ioc["IOC [USD/BHR]"]

        return ioc
    
    def __calculate_cash_operating_cost(self) -> dict:

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

        cash_operating_cost = {}

        cash_operating_cost["FUEL [USD/BHR]"]                   = fuel
        cash_operating_cost["ELECTRYCITY [USD/BHR]"]            = electric_energy
        cash_operating_cost["H2 [USD/BHR]"]                     = h2
        cash_operating_cost["COCKPIT CREW [USD/BHR]"]           = cockpit_crew
        cash_operating_cost["CABIN CREW [USD/BHR]"]             = cabin_crew
        cash_operating_cost["LANDING FEES [USD/BHR]"]           = landing_fees
        cash_operating_cost["NAVIGATION CHARGES [USD/BHR]"]     = nav_charges
        cash_operating_cost["GROUND HANDLING [USD/BHR]"]        = ground_charges
        cash_operating_cost["NOISE CHARGES [USD/BHR]"]          = noise_charges
        cash_operating_cost["NOX EMISSION CHARGES [USD/BHR]"]   = nox_emission_charges
        cash_operating_cost["CO EMISSION CHARGES [USD/BHR]"]    = co_emission_charges
        cash_operating_cost["CO2 EMISSION CHARGES [USD/BHR]"]   = co2_emission_charges
        cash_operating_cost["AIRFRANE MAINTENANCE [USD/BHR]"]   = airframe_maintenance
        cash_operating_cost["THERM. ENG. MAINTENANCE [USD/BH]"] = thermal_engine_maintenance

        cash_operating_cost["ELECTRIC MACHINE LINE MAINT. [USD/BH]"] = electric_machine_maint_line
        cash_operating_cost["ELECTRIC MACHINE BASE MAINT. [USD/BH]"] = electric_machine_maint_base
        cash_operating_cost["BATTERY LINE MAINT. [USD/BH]"]          = battery_maint_line 
        cash_operating_cost["BATTERY BASE MAINT. [USD/BH]"]          = battery_maint_base
        cash_operating_cost["FUEL CELL LINE MAINT. [USD/BH]"]        = fuelcell_maint_line 
        cash_operating_cost["FUEL CELL BASE MAINT. [USD/BH]"]        = fuelcell_maint_base 
        cash_operating_cost["POWER ELECTR. LINE MAINT. [USD/BH]"]    = power_elec_maint_line 
        cash_operating_cost["POWER ELECTR. BASE MAINT. [USD/BH]"]    = power_elec_maint_base       

        return cash_operating_cost
    
    def __calculate_financial_cost(self) -> dict:
        depr      = self.__calculate_depreciation()
        interest  = self.__calculate_interest()
        insurance = self.__calculate_insurance_cost()

        financial_costs = {}

        financial_costs["INSURANCE [USD/BHR]"]    = insurance
        financial_costs["DEPRECIATION [USD/BHR]"] = depr
        financial_costs["INTEREST [USD/BHR]"]     = interest

        return financial_costs
    
    def __calculate_co2_emission_charges(self) -> float:
        co2_value = self.aircraft["co2_value"]    
        prico2 = self.aircraft["prico2"]
        bt     = self.aircraft["bt"] 

        co2_emission_charges = (1.0-self.__params.AEC)*co2_value*prico2/bt
        return co2_emission_charges
    
    def __calculate_battery_maintenance_cost(self) -> tuple[float, float]:
        n_bat     = self.aircraft["n_bat"]
        n_repbat  = self.aircraft["n_repbat"]
        batprice = self.aircraft["batprice"]
        rvbat    = self.aircraft["rvbat"]
        lrbat    = self.aircraft["lrbat"]
        tlbat    = self.aircraft["tlbat"]
        f_bat     = self.aircraft["f_bat"]
        lifespan = self.aircraft["lifespan"]
        util     = self.aircraft["util"]

        battery_maint_line = n_bat*lrbat*tlbat*f_bat
        battery_maint_base = n_bat*(n_repbat*(batprice-rvbat))/(lifespan*util) # replace
        return battery_maint_line, battery_maint_base
    
    def __calculate_fuel_cell_maintenance_cost(self) -> tuple[float, float]:
        n_fc      = self.aircraft["n_fc"]
        n_repfc   = self.aircraft["n_repfc"]
        fcprice  = self.aircraft["fcprice"]
        rvfc     = self.aircraft["rvfc"]
        lrfc     = self.aircraft["lrfc"]
        tlfc     = self.aircraft["tlfc"]
        f_fc      = self.aircraft["f_fc"]
        lifespan = self.aircraft["lifespan"]
        util     = self.aircraft["util"]

        fuel_cell_maint_line = n_fc*lrfc*tlfc*f_fc
        fuel_cell_maint_base = n_fc*(n_repfc*(fcprice-rvfc))/(lifespan*util) # replace
        return fuel_cell_maint_line, fuel_cell_maint_base
    
    def __calculate_power_electronic_maintenance_cost(self) -> tuple[float, float]:
        n_reppe   = self.aircraft["n_reppe"]
        peprice  = self.aircraft["peprice"]
        rvpe     = self.aircraft["rvpe"]
        lrpe     = self.aircraft["lrpe"]
        tlpe     = self.aircraft["tlpe"]
        f_pe      = self.aircraft["f_pe"]
        lifespan = self.aircraft["lifespan"]
        util     = self.aircraft["util"]

        power_electronic_maint_line = lrpe*tlpe*f_pe
        power_electronic_maint_base = (n_reppe*(peprice-rvpe))/(lifespan*util) # replace
        return power_electronic_maint_line, power_electronic_maint_base

    def __calculate_electric_machine_maintenance_cost(self) -> tuple[float, float]:
        n_em      = self.aircraft["n_em"]     
        speml    = self.aircraft["speml"]       # spare parts cost line maintenance
        spemb    = self.aircraft["spemb"]       # spare parts cost base maintenance
        lrem     = self.aircraft["lrem"]
        tleml    = self.aircraft["tleml"]       # maintenance man hour line maint.
        tlemb    = self.aircraft["tlemb"]       # maintenance man hour base maint.
        f_eml     = self.aircraft["f_eml"]        # maintenance frequency line maint
        f_emb     = self.aircraft["f_emb"]        # maintenance frequency base maint
        lifespan = self.aircraft["lifespan"]
        util     = self.aircraft["util"]
        
        electric_machine_maint_line = n_em*(speml + lrem*tleml)*lifespan*f_eml/util
        electric_machine_maint_base = n_em*(spemb + lrem*tlemb)*f_emb*0.80
        return electric_machine_maint_line, electric_machine_maint_base
    
    def __calculate_airframe_maintenance_cost(self) -> float:
        n_bat     = self.aircraft["n_bat"]         
        n_em      = self.aircraft["n_em"]
        n_fc      = self.aircraft["n_fc"]
        batprice  = self.aircraft["batprice"]
        fcprice   = self.aircraft["fcprice"]
        emprice   = self.aircraft["emprice"]
        bt        = self.aircraft["bt"]
        adp       = self.aircraft["adp"]
        en        = self.aircraft["en"]
        enpri     = self.aircraft["enpri"]
        mew       = self.aircraft["mew"]
        bengw     = self.aircraft["bengw"]
        labor_rate = self.aircraft["labor_rate"]

        M   = 1.0 # Mach Number (Assumed 1 for subsonic cruise)
        FT  = bt - 0.25
        AFW = mew-(bengw*en)

        C_A_FH = 3.08*(adp - en*enpri - n_bat*batprice/1.0e6 - n_em*emprice/1.0e6 - n_fc*fcprice/1.0e6)
        C_A_FC = 6.24*(adp - en*enpri - n_bat*batprice/1.0e6 - n_em*emprice/1.0e6 - n_fc*fcprice/1.0e6)
        K_A_FC = 0.05*AFW*2.2 + 6 - 630.0/(AFW*2.2 + 120.0)
        K_A_FH = 0.59*K_A_FC
        
        airframe_labor_cost    = (K_A_FH*FT + K_A_FC)*labor_rate*math.sqrt(M)/bt
        airframe_material_cost = (C_A_FH*FT + C_A_FC)/bt

        airframe_maintenance_cost = airframe_material_cost + airframe_labor_cost
        return airframe_maintenance_cost

    def __calculate_thermal_engine_maintenance_cost(self) -> float:
        ieng = self.aircraft["ieng"]
        en   = self.aircraft["en"]
        
        if ieng == 1:
            bt    = self.aircraft["bt"]
            labor_rate    = self.aircraft["labor_rate"]
            shp   = self.aircraft["shp"]
            enpri = self.aircraft["enpri"]

            FT       = bt - 0.25
            K_ICE_FC = (0.3 + 0.03*shp/1000.0)*en
            K_ICE_FH = (0.65 + 0.03*shp/1000.0)*en
            C_ICE_FC = 2.0*en*enpri*10.0
            C_ICE_FH = 2.5*en*enpri*10.0

            thermal_engine_labor_cost    = (K_ICE_FH*FT + K_ICE_FC)*labor_rate/bt
            thermal_engine_material_cost = (C_ICE_FH*FT + C_ICE_FC)/bt

            thermal_engine_maintenance_cost = thermal_engine_material_cost + thermal_engine_labor_cost

        elif ieng == 2:
            eoc = self.aircraft["eoc"]

            thermal_engine_maintenance_cost = eoc*en
            
        else:
            raise ValueError(f"ieng Value {ieng} not valid")
        
        return thermal_engine_maintenance_cost
    
    def __calculate_nox_emission_charges(self) -> float:
        cnox        = self.aircraft["cnox"]
        nox_value = self.aircraft["nox_value"]
        bt           = self.aircraft["bt"]

        nox_emission_charges = (cnox*nox_value)/bt
        return nox_emission_charges

    def __calculate_co_emission_charges(self) -> float:
        cco         = self.aircraft["cco"]
        co_value  = self.aircraft["co_value"]
        bt           = self.aircraft["bt"]

        co_emission_charges  = (cco*co_value)/bt
        return co_emission_charges
    
    def __calculate_noise_charges(self) -> float:
        l_app   = self.aircraft["l_app"]
        ta      = self.aircraft["ta"]
        l_flyov = self.aircraft["l_flyov"]
        l_lat   = self.aircraft["l_lat"]
        td      = self.aircraft["td"]
        bt      = self.aircraft["bt"]
        cnoise  = self.aircraft["cnoise"]

        DELTAA = (l_app-ta)/10.0
        DELTAD = (((l_flyov+l_lat)/2.0)-td)/10.0
        
        noise_charges = (cnoise*(10.0**(DELTAA)+10.0**(DELTAD)))/bt
        return noise_charges

    def __calculate_ground_handling_charges(self) -> float:
        pld   = self.aircraft["pld"]
        bt    = self.aircraft["bt"]

        ground_charges = (self.__params.HTONN*pld)/bt
        return ground_charges
    
    def __calculate_navigation_charges(self) -> float:
        mtow   = self.aircraft["mtow"]
        bt     = self.aircraft["bt"]
        sector = self.aircraft["sector"]

        nav_charges = (self.__params.ENR*sector*1.853/100.0)*math.sqrt(mtow/50.0)/bt
        return nav_charges
    
    def __calculate_landing_fees(self) -> float:
        mtow = self.aircraft["mtow"]
        bt   = self.aircraft["bt"]

        landing_fees = (self.__params.LANDINGUR*mtow)/bt
        return landing_fees

    def __calculate_cabin_crew_cost(self) -> float:
        crcabhr = self.aircraft["crcabhr"]
        crewc   = self.aircraft["crewc"]

        cabin_crew = crcabhr*crewc
        return cabin_crew
    
    def __calculate_cockpit_crew_cost(self) -> float:
        crtechr  = self.aircraft["crtechr"]
        crewtech = self.aircraft["crewtech"]

        cockpit_crew = crtechr*crewtech
        return cockpit_crew
    
    def __calculate_h2_price(self) -> None:
        h2_pri         = self.aircraft["h2_pri"]
        h2_req = self.aircraft["h2_req"]
        bt            = self.aircraft["bt"]

        h2_price = h2_pri*h2_req/bt
        return h2_price
    
    def __calculate_electric_energy_price(self) -> None:
        enerpri         = self.aircraft["enerpri"]
        ener_req = self.aircraft["ener_req"]
        bt              = self.aircraft["bt"]

        electric_energy_price = ener_req*enerpri/bt
        return electric_energy_price
    
    def __calculate_fuel_cost(self) -> float:
        fuelpri = self.aircraft["fuelpri"]
        bf      = self.aircraft["bf"]
        bt      = self.aircraft["bt"]

        fuel = (0.328*fuelpri*bf)/bt
        return fuel
    
    def __calculate_insurance_cost(self) -> float:
        rinsh = self.aircraft["rinsh"]
        adp   = self.aircraft["adp"]*1.0e6
        util  = self.aircraft["util"]

        insurance = (rinsh*adp)/util
        return insurance
    
    def __calculate_investment(self) -> float:
        adp     = self.aircraft["adp"]*1.0e6
        afspare = self.aircraft["afspare"]
        enpri   = self.aircraft["enpri"]
        en      = self.aircraft["en"]
        enspare = self.aircraft["enspare"]

        invest = adp+(afspare*(adp-enpri*en))+(enspare*enpri*en)
        return invest
    
    def __calculate_interest(self) -> float:
        util = self.aircraft["util"]

        INVEST = self.__calculate_investment()
        
        interest = (0.053*INVEST)/util
        return interest
        
    def __calculate_depreciation(self) -> float:
        rval   = self.aircraft["rval"]
        dyrs   = self.aircraft["dyrs"]
        util   = self.aircraft["util"]

        INVEST = self.__calculate_investment()

        depr = ((1-rval)*INVEST)/(dyrs*util)
        return depr