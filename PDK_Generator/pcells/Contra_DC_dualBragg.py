from . import *

class Contra_DC_dualBragg(pya.PCellDeclarationHelper):
  """
  Author:   Mustafa Hammood 
                Mustafa@ece.ubc.ca
  """

  def __init__(self):

    # Important: initialize the super class
    super(Contra_DC_dualBragg, self).__init__()
    TECHNOLOGY = get_technology_by_name('{orig-techname}')

    # declare the parameters
    self.param("number_of_periods", self.TypeInt, "Number of grating periods (sidewall)", default = {n-periods-sidewall})
    self.param("number_of_periods_swg", self.TypeInt, "Number of grating periods (sub-wavelength)", default = {n-periods-swg})
    self.param("grating_period1", self.TypeDouble, "Grating period (microns)", default = {grating-period})
    self.param("grating_period2", self.TypeDouble, "Subwavelength Grating period (microns)", default = {swg-grating-period})
    self.param("gap", self.TypeDouble, "Gap (microns)", default = {gap})
    self.param("corrugation_width1", self.TypeDouble, "Waveguide 1 Corrugration width (microns)", default = {corrugation-width1})
    self.param("corrugation_width2", self.TypeDouble, "Waveguide 2 Corrugration width (microns)", default = {corrugation-width2})
    self.param("corrugation_width", self.TypeDouble, "Subwavelength Corrugration width (microns)", default = {swg-corrugation-width})
    self.param("AR", self.TypeBoolean, "Anti-Reflection Coating", default ={anti-reflection})
    self.param("sinusoidal", self.TypeBoolean, "Grating Type (Rectangular=False, Sinusoidal=True)", default = {grating-type})
    self.param("wg1_width", self.TypeDouble, "Waveguide 1 width", default = {waveguide1-width})
    self.param("wg2_width", self.TypeDouble, "Waveguide 2 width", default = {waveguide2-width})
    self.param("index", self.TypeDouble, "Gaussian Index", default = {gaussian-index})
    
    # declare layer params
    self.param("layer", self.TypeLayer, "Layer", default = TECHNOLOGY['{{Layer}Waveguide}'], hidden = True)
    self.param("pinrec", self.TypeLayer, "PinRec Layer", default = TECHNOLOGY['{{Layer}PinRec}'], hidden = True)
    self.param("devrec", self.TypeLayer, "DevRec Layer", default = TECHNOLOGY['{{Layer}DevRec}'], hidden = True)
    self.param("textl", self.TypeLayer, "Text Layer", default = TECHNOLOGY['{{Layer}Text}'], hidden = True)

  def display_text_impl(self):
    # Provide a descriptive text for the cell
    return "Contra_DC_dualBragg%s-%.3f" % \
    (self.number_of_periods, self.grating_period1)
  
  def coerce_parameters_impl(self):
    pass

  def can_create_from_shape(self, layout, shape, layer):
    return False
    
  def produce_impl(self):
  
    # fetch the parameters
    dbu = self.layout.dbu
    ly = self.layout
    shapes = self.cell.shapes

    LayerSi = self.layer
    LayerSiN = ly.layer(LayerSi)
    LayerPinRecN = ly.layer(self.pinrec)
    LayerDevRecN = ly.layer(self.devrec)

    from SiEPIC.extend import to_itype
    
    # Draw the Bragg grating (bottom):
    box_width = to_itype(self.grating_period1/2,dbu)
    SWG_width = to_itype(self.grating_period2/2,dbu)
    
    grating_period1 = to_itype(self.grating_period1,dbu)
    grating_period2 = to_itype(self.grating_period2,dbu)

    w = to_itype(self.wg1_width,dbu)
    GaussianIndex = self.index
    half_w = w/2
    half_corrugation_w = to_itype(self.corrugation_width1/2,dbu)
    
    
    N = self.number_of_periods
    
    vertical_offset1 = to_itype(self.gap/2 + self.wg1_width/2, dbu)
    vertical_offset2 = to_itype(-self.gap/2 - self.wg2_width/2, dbu)
    
  
    for i in range(0,self.number_of_periods):
      x = int(round((i * self.grating_period1)/dbu))
      
      profileFunction = math.exp( -0.5*(2*GaussianIndex*(i-N/2)/(N))**2 )
      profile = int(round(self.corrugation_width1/2/dbu))*profileFunction
      
      box1 = Box(x, vertical_offset1-half_w-profile, x + box_width, vertical_offset1+half_w-profile)
      
      box2 = Box(x + box_width, vertical_offset1-half_w+profile, x + 2*box_width, vertical_offset1+half_w+profile)
      
      shapes(LayerSiN).insert(box1)
      shapes(LayerSiN).insert(box2)
      
      length = x + grating_period1
    
    
    
    # Draw the Bragg grating (bottom):
    box_width = int(round(self.grating_period1/2/dbu))
    grating_period = int(round(self.grating_period1/dbu))
    w = to_itype(self.wg2_width,dbu)
    GaussianIndex = self.index
    half_w = w/2
    half_corrugation_w = int(round(self.corrugation_width2/2/dbu))
    
    for i in range(0,self.number_of_periods):
      x = int(round((i * self.grating_period1)/dbu))
      
      profileFunction = math.exp( -0.5*(2*GaussianIndex*(i-N/2)/(N))**2 )
      profile = int(round(self.corrugation_width2/2/dbu))*profileFunction
      
      box1 = Box(x, vertical_offset2-half_w-profile, x + box_width, vertical_offset2+half_w-profile)
      
      box2 = Box(x + box_width, vertical_offset2-half_w+profile, x + 2*box_width, vertical_offset2+half_w+profile)
      
      shapes(LayerSiN).insert(box1)
      shapes(LayerSiN).insert(box2)
      
      length = x + grating_period1      
      
    # Draw the Bragg grating (SWG):
    vertical_offset = (int(round(self.corrugation_width2/dbu))-int(round(self.corrugation_width1/dbu)))/4
    
    box_width = int(round(self.grating_period2/2/dbu))
    grating_period = int(round(self.grating_period2/dbu))
    w = to_itype(self.corrugation_width,dbu)
    GaussianIndex = self.index
    half_corrugation_w = int(round(self.corrugation_width/dbu))
    
    for i in range(0,self.number_of_periods_swg):
      x_swg = int(round((i * self.grating_period2)/dbu))
      
      profileFunction = math.exp( -0.5*(2*GaussianIndex*(i-N/2)/(N))**2 )
      profile = int(round(self.corrugation_width/dbu))*profileFunction
      
      box1 = Box(x_swg, vertical_offset+w/2+profile, x_swg + box_width, vertical_offset-w/2-profile)
      
      shapes(LayerSiN).insert(box1)
      
      length_swg = x + grating_period2
      
      
    # Create the pins on the waveguides, as short paths:
    from SiEPIC._globals import PIN_LENGTH as pin_length

    w = to_itype(self.wg2_width,dbu)
    t = Trans(Trans.R0, 0,vertical_offset2)
    pin = Path([Point(pin_length/2, 0), Point(-pin_length/2, 0)], w)
    pin_t = pin.transformed(t)
    shapes(LayerPinRecN).insert(pin_t)
    text = Text ("pin1", t)
    shape = shapes(LayerPinRecN).insert(text)
    shape.text_size = 0.4/dbu
    
    w = to_itype(self.wg1_width,dbu)
    t = Trans(Trans.R0, 0,vertical_offset1)
    pin = Path([Point(pin_length/2, 0), Point(-pin_length/2, 0)], w)
    pin_t = pin.transformed(t)
    shapes(LayerPinRecN).insert(pin_t)
    text = Text ("pin3", t)
    shape = shapes(LayerPinRecN).insert(text)
    shape.text_size = 0.4/dbu

    w = to_itype(self.wg1_width,dbu)
    t = Trans(Trans.R0, length,vertical_offset1)
    pin = Path([Point(-pin_length/2, 0), Point(pin_length/2, 0)], w)
    pin_t = pin.transformed(t)
    shapes(LayerPinRecN).insert(pin_t)
    text = Text ("pin2", t)
    shape = shapes(LayerPinRecN).insert(text)
    shape.text_size = 0.4/dbu
    
    w = to_itype(self.wg2_width,dbu)
    t = Trans(Trans.R0, length,vertical_offset2)
    pin = Path([Point(-pin_length/2, 0), Point(pin_length/2, 0)], w)
    pin_t = pin.transformed(t)
    shapes(LayerPinRecN).insert(pin_t)
    text = Text ("pin4", t)
    shape = shapes(LayerPinRecN).insert(text)
    shape.text_size = 0.4/dbu

    # Compact model information
    t = Trans(Trans.R0, 0, 0)
    text = Text ('Lumerical_INTERCONNECT_library=Design kits/{orig-techname}', t)
    shape = shapes(LayerDevRecN).insert(text)
    shape.text_size = 0.1/dbu
    t = Trans(Trans.R0, length/10, 0)
    text = Text ('Component={cm-name}', t)
    shape = shapes(LayerDevRecN).insert(text)
    shape.text_size = 0.1/dbu
    t = Trans(Trans.R0, length/9, 0)
    text = Text \
      ('Spice_param:number_of_periods=%s grating_period=%.3fu corrugation_width=%.3fu sinusoidal=%s' %\
      (self.number_of_periods, self.grating_period1, self.corrugation_width1, int(self.sinusoidal)), t )
    shape = shapes(LayerDevRecN).insert(text)
    shape.text_size = 0.1/dbu

    # Create the device recognition layer -- make it 1 * wg_width away from the waveguides.
    t = Trans(Trans.R0, 0,0)
    path = Path([Point(0, 0), Point(length, 0)], 3*w)
    shapes(LayerDevRecN).insert(path.simple_polygon())
    
