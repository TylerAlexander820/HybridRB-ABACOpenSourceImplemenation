package smartHomeAuthorization

default allow_access = false

allow_access if {
  "shParent" == input.role 
  "Thermostat" == input.deviceName
  input.temperature >= 10
  input.temperature <= 40
}

allow_access if {
  "shParent" == input.role 
   input.deviceName in {"smartLightM","smartLightsB"}
   lower(input.state) in {"true", "false"}
}

allow_access if {
  "shParent" == input.role 
   "frontDoor" == input.deviceName 
   lower(input.state) in {"true", "false"}
}

#Toggle Oven Power
allow_access if {
  "shParent" == input.role 
   "smartOven" == input.deviceName
   lower(input.ovenPower) in {"true", "false"}
   input.temperature <= 550
}

#Change temp if Oven is on
allow_access if {
  "shParent" == input.role 
   "smartOven" == input.deviceName
   lower(input.ovenPower) == "true"
   input.temperature <= 550
}

allow_access if {
  "shTeen" == input.role 
  "Thermostat" == input.deviceName
  input.temperature >= 20
  input.temperature <= 30
}

allow_access if {
  "shTeen" == input.role 
   input.deviceName in {"smartLightM","smartLightsB"}
   lower(input.state) in {"true", "false"}
}

allow_access if {
  "shTeen" == input.role 
   "frontDoor" == input.deviceName 
   lower(input.state) in {"true", "false"}
   input.currentHour >= 8
   input.currentHour < 19
}

#Toggle Oven Power
allow_access if {
  "shTeen" == input.role 
   "smartOven" == input.deviceName
   lower(input.ovenPower) in {"true", "false"}
   input.temperature <= 550
}

#Change temp if Oven is on
allow_access if {
  "shTeen" == input.role 
  "smartOven" == input.deviceName
   lower(input.ovenPower) == "true"
   input.temperature <= 550
}

allow_access if {
  "shChild" == input.role 
   input.state
   "frontDoor" == input.deviceName 
   lower(input.state) in {"true", "false"}
    input.currentHour >= 8
    input.currentHour < 17
}

allow_access if {
  "shChild" == input.role 
   input.deviceName in {"smartLightM","smartLightsB"}
   lower(input.state) in {"true", "false"}
}

allow_access if {
  "shChild" == input.role 
   "smartOven" == input.deviceName
   lower(input.ovenPower) in {"true", "false"}
   input.parentApproval == "true"
   input.temperature <= 550
}

allow_access if {
  "shChild" == input.role 
   "smartOven" == input.deviceName
   lower(input.ovenPower) in {"true", "false"}
   input.currentMonth = 12
   input.temperature <= 550
}

#Change temp if Oven is on
allow_access if {
   "shChild" == input.role 
   "smartOven" == input.deviceName
   lower(input.ovenPower) == "true"
   input.parentApproval == "true"
   input.temperature <= 550
}

#Change temp if Oven is on and month is 12
allow_access if {
   "shChild" == input.role 
   "smartOven" == input.deviceName
   lower(input.ovenPower) == "true"
   input.temperature <= 550
   input.currentMonth = 12
}
