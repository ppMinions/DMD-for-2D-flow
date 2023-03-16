#!MC 1410

$!VarSet |NUMLOOP|= 4245
$!LOOP 150
$!VarSet |NUMLOOP| += 5

$!ReadDataSet  '"STANDARDSYNTAX" "1.0" "FILENAME_FILE" "F:\local_membrane_airfoil\cylinyder_dmd\data\flow_0|NUMLOOP|.szplt"'
  DataSetReader = 'Tecplot Subzone Data Loader'
  ReadDataOption = New
  ResetStyle = No
  AssignStrandIDs = No
  InitialPlotType = Automatic
  InitialPlotFirstZoneOnly = No
  AddZonesToExistingStrands = No
  VarLoadMode = ByName
$!ExtendedCommand 
  CommandProcessorID = 'CFDAnalyzer4'
  Command = 'SetFieldVariables ConvectionVarsAreMomentum=\'T\' UVarNum=4 VVarNum=5 WVarNum=0 ID1=\'Pressure\' Variable1=7 ID2=\'Temperature\' Variable2=8'
$!ExtendedCommand 
  CommandProcessorID = 'CFDAnalyzer4'
  Command = 'Calculate Function=\'ZVORTICITY\' Normalization=\'None\' ValueLocation=\'Nodal\' CalculateOnDemand=\'T\' UseMorePointsForFEGradientCalculations=\'F\''
$!WriteDataSet  "F:\local_membrane_airfoil\cylinyder_dmd\data\flow_0|NUMLOOP|.dat"
  IncludeText = No
  IncludeGeom = No
  IncludeDataShareLinkage = Yes
  VarList =  [1-2,16]
  Binary = No
  UsePointFormat = Yes
  Precision = 9
  TecplotVersionToWrite = TecplotCurrent
$!Page Name = 'Untitled'
$!PageControl Create
$!NewLayout 
$!ENDLOOP
