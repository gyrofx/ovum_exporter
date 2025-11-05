import json

from prometheus_client import Gauge

from ovum_exporter.ovum import read_ovum
from dataclasses import dataclass

def find_descriptor_text_from_parameter(parameter):
    from ovum_exporter.ovum import descriptor
    lang = 'en'
    matching_item = next((item for item in descriptor if f"{item['parameter']}" == parameter),None)
    descriptor_text = matching_item.get("tlangalphakey", {}).get(lang, "") if matching_item else ""
    return descriptor_text


@dataclass
class GaugeMetrics:
    register: int
    parameter: str
    metric_name: str
    description: str = ""
    metrics: Gauge = None

    def __post_init__(self):
        self.metrics = Gauge(self.metric_name, self.description)
        # if not self.description:
        #     self.description = find_descriptor_text_from_parameter(self.parameter)
    


def init_metrics():
    global _registers
    _registers = [
        GaugeMetrics(12308, 'Rps ', 'ovum_inverter_rps'),  #          Rps             50              rps             Inverter RPS set
        # GaugeMetrics(12318, 'HS  ', 'ovum_main_switch'),  #          HS              ON                              Main switch
        # GaugeMetrics(12328, 'ALAR', 'ovum_active_alarm'),  #          ALAR            No                              Active Alarm
        # GaugeMetrics(12338, 'Anfo', 'ovum_operating_mode'),  #          Anfo            HEATING                         Operating Mode
        GaugeMetrics(12348, 'CoMi', 'ovum_running_time'),  #          CoMi            2               min             Running time
        GaugeMetrics(12358, 'CoHo', 'ovum_working_hours'),  #          CoHo            36              h               Working hours
        GaugeMetrics(12368, 'HePw', 'ovum_heating_power'),  #          HePw            6.03            kW              Heating power

        GaugeMetrics(12388, 'ATvz', 'ovum_ambient_temperature_avg'),  #          ATvz            10.9            °C              Ambient.t.avg.
        GaugeMetrics(14608, 'AI9s', 'ovum_outdoor_temperature'),            # 14608           AI9s            80              1               8.0             °C              0                               -32768          32767           True            False           4598            Outdoor temp

        GaugeMetrics(12398, 'ReTe', 'ovum_controller_temperature'),  #          ReTe            39.8            °C              Controler temperature
        GaugeMetrics(12408, 'Spo ', 'ovum_dhw_tank_upper_temperature'),  #          Spo             47.8            °C              Temp. DHW-Tank upper
        GaugeMetrics(12418, 'Spm ', 'ovum_dhw_tank_middle_temperature'),  #          Spm             47.1            °C              Temp. DHW-Tank middle
        GaugeMetrics(12428, 'Spu ', 'ovum_dhw_tank_lower_temperature'),  #          Spu             30.9            °C              Temp. Heating Tank lower

        GaugeMetrics(12528, 'HeaW', 'ovum_weekly_heating_energy'),  #          HeaW            153.06          kWh             Weekly
        GaugeMetrics(12538, 'HeaM', 'ovum_monthly_heating_energy'),  #          HeaM            85.47           kWh             Monthly
        GaugeMetrics(12548, 'HeaY', 'ovum_yearly_heating_energy'),  #          HeaY            153.06          kWh             Yearly
        GaugeMetrics(12558, 'HeaT', 'ovum_total_heating_energy'),  #          HeaT            153.06          kWh             Total
        # GaugeMetrics(12568, 'COP ', 'ovum_cop'),  #          COP                                             COP
        GaugeMetrics(12578, 'COPW', 'ovum_cop_weekly'),  #          COPW            5.3                             Weekly
        GaugeMetrics(12588, 'COPM', 'ovum_cop_monthly'),  #          COPM            5.2                             Monthly
        GaugeMetrics(12598, 'COPY', 'ovum_cop_yearly'),  #          COPY            5.3                             Yearly
        GaugeMetrics(12608, 'TOTA', 'ovum_cop_total'),  #          TOTA            5.3                             Total

        GaugeMetrics(12988, 'EQin', 'ovum_ground_source_in'),                          # 12988           EQin            12.7            °C              ES in
        GaugeMetrics(12998, 'EQou', 'ovum_ground_source_out'),                         # 12998           EQou            9.6             °C              ES out
        GaugeMetrics(13008, 'AO02', 'ovum_ground_source_pump'),                        # 13008           AO02            70.0            %               ES pump

        GaugeMetrics(13488, 'DrTm', 'ovum_drive_temperature'),              # 13488           DrTm            33              °C              Drive temperature
        GaugeMetrics(13498, 'DrKw', 'ovum_inverter_power'),                 # 13498           DrKw            0.85            kW              Inverter power

        GaugeMetrics(13898, 'AI07', 'ovum_heat_circle_1_flow_temperature'),         # 13898           AI07            31.0            °C              HEAC1 flow temp.
        GaugeMetrics(13918, 'AI08', 'ovum_heat_circle_1_return_temperature'),       # 13918           AI08            28.9            °C              HEAC1 return temp.
        GaugeMetrics(14848, 'HReS', 'ovum_heat_circle_1_return_set_temperature'),   # 14848           HReS            287             1               28.7            °C              0                               0               45.0            True            False           4611            Return set temperature
        GaugeMetrics(14898, 'AO11', 'ovum_heat_circle_1_pump'),                     # 14898           AO11            7000            2               70.0            %               13                              -32768          32767           True            False           4607            HEAC 1 pump
        

        GaugeMetrics(15538, 'DoTs', 'ovum_tap_water_temperature'),          # 15538           DoTs            47.0            °C              Tap water
        GaugeMetrics(15548, 'DoT',  'ovum_tap_act_temperature'),            # 15548           DoT             45.9            °C              Tap act.
        GaugeMetrics(15578, 'FpMi', 'ovum_tap_pump_min'),                   # 15578           FpMi            16.0            %               Pumpe min
        GaugeMetrics(15448, 'SpTo', 'ovum_tap_pump_percent'), # 15588           vPID            0               2               0.0             %               13                              0               100.0           True            False           4807            FWT pump

    ]

    print(_registers)
    
def read_exporter_values(client, slave):
    for metrics in _registers:
        result = read_ovum(client, metrics.register, slave=slave)
        if result:
            metrics.metrics.set(result['value_float'])
            print(f'metrics {metrics.metrics} updated to {result["value_float"]}')



# 12308           Rps             50              rps             Inverter RPS set
# 12318           HS              ON                              Main switch
# 12328           ALAR            No                              Active Alarm
# 12338           Anfo            HEATING                         Operating Mode
# 12348           CoMi            2               min             Running time
# 12358           CoHo            36              h               Working hours
# 12368           HePw            6.03            kW              Heating power

# 12388           ATvz            10.9            °C              Ambient.t.avg.
# 12398           ReTe            39.8            °C              Controler temperature
# 12408           Spo             47.8            °C              Temp. DHW-Tank upper
# 12418           Spm             47.1            °C              Temp. DHW-Tank middle
# 12428           Spu             30.9            °C              Temp. Heating Tank lower


# 12528           HeaW            153.06          kWh             Weekly
# 12538           HeaM            85.47           kWh             Monthly
# 12548           HeaY            153.06          kWh             Yearly
# 12558           HeaT            153.06          kWh             Total
# 12568           COP                                             COP
# 12578           COPW            5.3                             Weekly
# 12588           COPM            5.2                             Monthly
# 12598           COPY            5.3                             Yearly
# 12608           TOTA            5.3                             Total


# 12628           SerN            3400981                         Serial number
# 12638           ID:             41444073                        ID Controller
# 12648           Vers            90646                           Software Version
# 12658           EQty            brine to water                  Energy source type
# 12668           CoNr            (6) NHWP06S                     Machine Configuration
# 12688           ManM            No                              Values in manual mode

# 12798           SpMo            buffer tank                     Request mode heatpump

# 12988           EQin            12.7            °C              ES in
# 12998           EQou            9.6             °C              ES out
# 13008           AO02            70.0            %               ES pump

# 13468           DrAl            Inactive                        Drive in alarm

# 13488           DrTm            33              °C              Drive temperature
# 13498           DrKw            0.85            kW              Inverter power 

# 13898           AI07            31.0            °C              HEAC1 flow temp.
# 13918           AI08            28.9            °C              HEAC1 return temp.
# 13938           AI09            11.1            °C              Outdoor temp

# 15538           DoTs            47.0            °C              Tap water
# 15548           DoT             45.9            °C              Tap act.
# 15448           SpTo            47.8            °C              Temp. DHW-Tank upper
# 15458           SpTm            47.1            °C              Temp. DHW-Tank middle
# 15578           FpMi            16.0            %               Pumpe min


# 16548           A_2             Inactive                        Hotgas temp.sensor
# 16558           A_3             Inactive                        Evaporation Temperature Probe Error
# 16568           A_4             Inactive                        Active alarm
# 16578           A_5             Inactive                        Active alarm
# 16588           A_6             Inactive                        Flow temperature sensor
# 16598           A_7             Inactive                        Active alarm
# 16608           A_8             Inactive                        Active alarm
# 16618           A_17            Inactive                        Controller Temp.Log
# 16628           A_18            Inactive                        Modbus error electr.count.
# 16638           A_19            Inactive                        CAN EEV warning
# 16648           A_20            Inactive                        CAN EEV OFF
# 16658           A_21            Inactive                        Max.Tank Temp
# 16668           A_32            Inactive                        FWS flow switch fault
# 16678           A_33            Inactive                        FWS  flwo temp sensor fault
# 16688           A_34            Inactive                        Sensor error controller
# 16698           A_35            Inactive                        Sensor error tank DHW
# 16708           A_36            Inactive                        Sensor error tank heat
# 16718           A_49            Inactive                        Sensor error LP transmitter
# 16728           A_50            Inactive                        Sensor error HP transmitter
# 16738           A_51            Inactive                        Inverter MB error
# 16748           A_52            Inactive                        Condensing temperature error
# 16758           A_53            Inactive                        Condensing pressure error
# 16768           A_54            Inactive                        Evaporation pressure error
# 16778           A_55            Inactive                        HG temp. Max. fault
# 16788           A_56            Inactive                        HG control difference fault
# 16798           A_57            Inactive                        LP HP difference fault
# 16808           A_58            Inactive                        suction gas temp min. fault
# 16818           A_59            Inactive                        ES set different fault
# 16828           A_60            Inactive                        Es out min fault
# 16838           A_61            Inactive                        ES flow sensor fault
# 16848           A_62            Inactive                        Inverter MB error
# 16858           A_63            Inactive                        Inverter-error
# 16868           A_64            Inactive                        ES-Motor protection
# 16878           A_65            Inactive                        Ventilation error
# 16888           A_66            Inactive                        Ventilation filter fault
# 16898           A_67            Inactive                        Max.Temp.error tank WW middle
# 16908           A_68            Inactive                        Min.Temp.error tank WW middle
# 16918           A_69            Inactive                        Max.Temp.error tank HEA
# 16928           A_70            Inactive                        Min.Temp.error tank HEA
# 16938           A_71            Inactive                        Max.Temp.error tank WW above
# 16948           A_72            Inactive                        Min.Temp.error tank WW above
# 16958           A_73            Inactive                        Max.Temp.error controller
# 16968           A_74            Inactive                        Min.Temp.error controller
# 16978           A_75            Inactive                        Max.Temp.error FWS flow
# 16988           A_76            Inactive                        Min.Temp.error FWS flow
# 16998           A_77            Inactive                        Max.Temp.error ambient
# 17008           A_78            Inactive                        Min.Temp.error ambient
# 17018           A_79            Inactive                        Max.Temp.error HC1 return
# 17028           A_80            Inactive                        Min.Temp.error HC1 return
# 17038           A_81            Inactive                        LP transmitter cooling fault
# 17048           A_82            Inactive                        Max.Restart is over
# 17058           A_83            Inactive                        Max.Presure.error LP
# 17068           A_84            Inactive                        Min.Presure.error LP
# 17078           A_85            Inactive                        Max.Presure.error HP
# 17088           A_86            Inactive                        Min.Presure.error HP
# 17098           A_87            Inactive                        Max.Temp.error HG
# 17108           A_88            Inactive                        Min.Temp.error HG
# 17118           A_89            Inactive                        Max.Temp.error SG
# 17128           A_90            Inactive                        Min.Temp.error SG
# 17138           A_91            Inactive                        Max.Temp.error ES-in
# 17148           A_92            Inactive                        Min.Temp.error ES-in
# 17158           A_93            Inactive                        Max.Temp.error ES-out
# 17168           A_94            Inactive                        Min.Temp.error ES-out
# 17178           A_95            Inactive                        Max.Temp.error HC1 flow
# 17188           A_96            Inactive                        Min.Temp.error HC1 flow