from . import *



class ebeam_dc_halfring_straight(pya.PCellDeclarationHelper):
  """
  The PCell declaration for the ebeam_dc_halfring_straight.
  Consists of a half-ring with 1 waveguides.
  """

  def __init__(self):
    # Important: initialize the super class
    super(ebeam_dc_halfring_straight, self).__init__()
    TECHNOLOGY = get_technology_by_name('{orig-techname}')
    TECHDRC = DRC(drc_yaml_file_location)

    # declare design parameters
    self.param("r", self.TypeDouble, "Radius", default = {radius})
    self.param("w", self.TypeDouble, "Waveguide Width", default = {waveguide-width})
    self.param("g", self.TypeDouble, "Gap", default = {gap})
    self.param("Lc", self.TypeDouble, "Coupler Length", default = {coupler-length})
    self.param("orthogonal_identifier", self.TypeInt, "Orthogonal identifier (1=TE, 2=TM)", default = {orthogonal-id})    

    # declare layer params
    self.param("silayer", self.TypeLayer, "Si Layer", default = TECHNOLOGY['{{Layer}Waveguide}'], hidden = True)
    self.param("pinrec", self.TypeLayer, "PinRec Layer", default = TECHNOLOGY['{{Layer}PinRec}'], hidden = True)
    self.param("devrec", self.TypeLayer, "DevRec Layer", default = TECHNOLOGY['{{Layer}DevRec}'], hidden = True)
    self.param("textl", self.TypeLayer, "Text Layer", default = TECHNOLOGY['{{Layer}Text}'], hidden = True)

  def display_text_impl(self):
    # Provide a descriptive text for the cell
    return "ebeam_dc_halfring_straight(R=" + ('%.3f' % self.r) + ",g=" + ('%g' % (1000*self.g)) + ",Lc=" + ('%g' % (1000*self.Lc)) + ",orthogonal_identifier=" + ('%s' % self.orthogonal_identifier) + ")"

  def can_create_from_shape_impl(self):
    return False
    
  def produce_impl(self):
    # This is the main part of the implementation: create the layout

    from math import pi, cos, sin
    from SiEPIC.utils import arc_wg, arc_wg_xy
    from SiEPIC._globals import PIN_LENGTH

    # fetch the parameters
    dbu = self.layout.dbu
    ly = self.layout
    shapes = self.cell.shapes
    
    LayerSiN = ly.layer(self.silayer)
    LayerPinRecN = ly.layer(self.pinrec)
    LayerDevRecN = ly.layer(self.devrec)
    TextLayerN = ly.layer(self.textl)

    w = int(round(self.w/dbu))
    r = int(round(self.r/dbu))
    g = int(round(self.g/dbu))
    Lc = int(round(self.Lc/dbu))

    # draw the half-circle
    x = 0
    y = r+w+g
    self.cell.shapes(LayerSiN).insert(arc_wg_xy(x-Lc/2, y, r, w, 180, 270))
    self.cell.shapes(LayerSiN).insert(arc_wg_xy(x+Lc/2, y, r, w, 270, 360))
    
    # Pins on the top side:
    pin = Path([Point(-r-Lc/2, y-PIN_LENGTH/2), Point(-r-Lc/2, y+PIN_LENGTH/2)], w)
    shapes(LayerPinRecN).insert(pin)
    t = Trans(Trans.R0, -r-Lc/2, y)
    text = Text ("pin2", t)
    shape = shapes(LayerPinRecN).insert(text)
    shape.text_size = 0.4/dbu

    pin = Path([Point(r+Lc/2, y-PIN_LENGTH/2), Point(r+Lc/2, y+PIN_LENGTH/2)], w)
    shapes(LayerPinRecN).insert(pin)
    t = Trans(Trans.R0, r+Lc/2, y)
    text = Text ("pin4", t)
    shape = shapes(LayerPinRecN).insert(text)
    shape.text_size = 0.4/dbu

    if Lc > 0:
      wg1 = Box(-Lc/2, -w/2+w+g, Lc/2, w/2+w+g)
      shapes(LayerSiN).insert(wg1)


    # Create the waveguide
    wg1 = Box(-r-w/2-w-Lc/2, -w/2, r+w/2+w+Lc/2, w/2)
    shapes(LayerSiN).insert(wg1)

    # Pins on the bus waveguide side:
    pin = Path([Point(-r-w/2-w+PIN_LENGTH/2-Lc/2, 0), Point(-r-w/2-w-PIN_LENGTH/2-Lc/2, 0)], w)
    shapes(LayerPinRecN).insert(pin)
    t = Trans(Trans.R0, -r-w/2-w-Lc/2, 0)
    text = Text ("pin1", t)
    shape = shapes(LayerPinRecN).insert(text)
    shape.text_size = 0.4/dbu

    pin = Path([Point(r+w/2+w-PIN_LENGTH/2+Lc/2, 0), Point(r+w/2+w+PIN_LENGTH/2+Lc/2, 0)], w)
    shapes(LayerPinRecN).insert(pin)
    t = Trans(Trans.R0, r+w/2+w+Lc/2, 0)
    text = Text ("pin3", t)
    shape = shapes(LayerPinRecN).insert(text)
    shape.text_size = 0.4/dbu

    # Merge all the waveguide shapes, to avoid any small gaps
    layer_temp = self.layout.layer(LayerInfo(913, 0))
    shapes_temp = self.cell.shapes(layer_temp)
    ShapeProcessor().merge(self.layout,self.cell,LayerSiN,shapes_temp,True,0,True,True)
    self.cell.shapes(LayerSiN).clear()
    shapes_SiN = self.cell.shapes(LayerSiN)
    ShapeProcessor().merge(self.layout,self.cell,layer_temp, shapes_SiN,True,0,True,True)
    self.cell.shapes(layer_temp).clear()

    # Create the device recognition layer -- make it 1 * wg_width away from the waveguides.
    dev = Box(-r-w/2-w-Lc/2, -w/2-w, r+w/2+w+Lc/2, y )
    shapes(LayerDevRecN).insert(dev)

    # Compact model information
    t = Trans(Trans.R0, -r, 0)
    text = Text ("Lumerical_INTERCONNECT_library=Design kits/{orig-techname}", t)
    shape = shapes(LayerDevRecN).insert(text)
    shape.text_size = self.r*0.03/dbu

    t = Trans(Trans.R0, -r, r/4)
    text = Text ('Component={cm-name}', t)
    shape = shapes(LayerDevRecN).insert(text)
    shape.text_size = self.r*0.03/dbu

    t = Trans(Trans.R0, -r, r/2)
    text = Text ('Spice_param:wg_width=%.3g gap=%.3g radius=%.3g Lc=%.3g orthogonal_identifier=%s'% (self.w*1e-6,self.g*1e-6,self.r*1e-6,self.Lc*1e-6, self.orthogonal_identifier), t)
    shape = shapes(LayerDevRecN).insert(text)
    shape.text_size = self.r*0.03/dbu

    print("Done drawing the layout for - ebeam_dc_halfring_straight: %.3f-%g" % ( self.r, self.g) )
